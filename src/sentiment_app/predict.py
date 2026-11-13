"""Fonction publique de prédiction, alimentée par la ressource du paquet installé."""

import os
from functools import lru_cache
from importlib.resources import files
from pathlib import Path
from typing import Literal, TypedDict

import joblib

RACINE = Path(__file__).resolve().parents[2]
RESSOURCE_MODELE = files("sentiment_app").joinpath("modele/sentiment.joblib")
MODELE_PAQUET = Path(str(RESSOURCE_MODELE))
MODELE_DEVELOPPEMENT = RACINE / "models" / "sentiment.joblib"
MODELE = MODELE_PAQUET if MODELE_PAQUET.is_file() else MODELE_DEVELOPPEMENT


class Prediction(TypedDict):
    label: Literal["positive", "negative"]
    score: float


@lru_cache(maxsize=1)
def charger_modele():
    """Charge une fois le modèle embarqué, ou l'artefact local en développement."""
    chemin_env = os.environ.get("SENTIMENT_MODELE")
    if chemin_env:
        chemin = Path(chemin_env)
        if not chemin.is_file():
            raise FileNotFoundError(f"Modèle indiqué par SENTIMENT_MODELE introuvable : {chemin}")
        return joblib.load(chemin)

    if MODELE == MODELE_PAQUET:
        with RESSOURCE_MODELE.open("rb") as fichier:
            return joblib.load(fichier)
    if not MODELE.is_file():
        raise FileNotFoundError(
            "models/sentiment.joblib absent : lancez python src/train.py "
            "ou installez une roue qui embarque le modèle."
        )
    return joblib.load(MODELE)


def predict(texte: str) -> Prediction:
    """Renvoie l'étiquette et le score du modèle pour un avis."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    pipeline = charger_modele()
    etiquette = pipeline.predict([texte])[0]
    score = float(pipeline.predict_proba([texte]).max())
    return {"label": etiquette, "score": round(score, 4)}
