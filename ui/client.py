"""Client HTTP de l'API versionnée : l'interface ne connaît pas le modèle.

La configuration vient de .env ou de l'environnement : API_URL et API_KEY.
"""
import os
from collections import Counter
from dataclasses import dataclass

import httpx
from dotenv import load_dotenv

load_dotenv()

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")
API_KEY = os.environ.get("API_KEY", "")
VERDICTS = {
    "POSITIVE": "Avis positif",
    "NEGATIVE": "Avis négatif",
    "INDETERMINE": "Je ne sais pas : à faire vérifier par un humain",
}
INJOIGNABLE = "API injoignable : lancez d'abord uvicorn api.main:app"
REFUS = "Texte refusé : vide, fait d'espaces, ou de plus de 2000 caractères."
SANS_MODELE = "Modèle non chargé : python src/train.py, puis relancer l'API."
CLE = "Clé d'API absente ou refusée : configurez API_KEY dans .env."


@dataclass
class Reponse:
    """Ce que l'interface affiche : un verdict, ou un message d'erreur lisible."""

    ok: bool
    label: str | None = None
    score: float | None = None
    message: str = ""


def creer_session() -> httpx.Client:
    """La connexion à l'API, avec la clé client chargée côté serveur Streamlit."""
    return httpx.Client(base_url=API_URL, timeout=10)


def _headers() -> dict[str, str]:
    return {"X-API-Key": API_KEY} if API_KEY else {}


def _code_erreur(reponse: httpx.Response) -> str:
    try:
        return str(reponse.json()["erreur"]["code"])
    except (ValueError, KeyError, TypeError):
        return ""


def sante(session: httpx.Client) -> Reponse:
    try:
        r = session.get("/v1/health", headers=_headers())
    except httpx.TransportError:
        return Reponse(False, message=INJOIGNABLE)
    if r.status_code == 200:
        return Reponse(True, message=r.json()["model"])
    code = _code_erreur(r)
    if code == "MODELE_INDISPONIBLE":
        return Reponse(False, message=SANS_MODELE)
    if code in {"NON_AUTHENTIFIE", "ACCES_REFUSE"}:
        return Reponse(False, message=CLE)
    return Reponse(False, message=f"Erreur de l'API ({r.status_code}).")


def predire(session: httpx.Client, texte: str) -> Reponse:
    try:
        r = session.post("/v1/predict", json={"text": texte}, headers=_headers())
    except httpx.TransportError:
        return Reponse(False, message=INJOIGNABLE)
    if r.status_code == 200:
        corps = r.json()
        return Reponse(True, label=corps["label"], score=corps["score"])
    code = _code_erreur(r)
    if code == "ENTREE_INVALIDE":
        return Reponse(False, message=REFUS)
    if code == "MODELE_INDISPONIBLE":
        return Reponse(False, message=SANS_MODELE)
    if code in {"NON_AUTHENTIFIE", "ACCES_REFUSE"}:
        return Reponse(False, message=CLE)
    return Reponse(False, message=f"Erreur interne de l'API ({r.status_code}).")


def predire_lot(session: httpx.Client, textes: list[str]) -> list[Reponse]:
    return [predire(session, texte) for texte in textes]


def resumer(reponses: list[Reponse]) -> dict[str, int]:
    """Nombre d'avis par verdict ; les refus et les erreurs sont comptés à part."""
    compte = Counter(
        r.label if r.ok and r.label is not None else "REFUS OU ERREUR" for r in reponses
    )
    return dict(sorted(compte.items()))
