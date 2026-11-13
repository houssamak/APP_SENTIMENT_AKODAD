"""Chargement et prédiction du modèle de sentiment."""

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal, TypedDict

import joblib

RACINE = Path(__file__).resolve().parents[1]


def chemin_modele() -> Path:
    """Retourne SENTIMENT_MODELE, ou le modèle attendu dans le dépôt."""
    return Path(os.environ.get("SENTIMENT_MODELE") or RACINE / "models" / "sentiment.joblib")


MODELE = chemin_modele()


class Prediction(TypedDict):
    label: Literal["positive", "negative"]
    score: float


@lru_cache(maxsize=1)
def charger_modele():
    """Charge le modèle une fois par processus."""
    if not MODELE.exists():
        raise FileNotFoundError(
            f"models/sentiment.joblib absent (modèle recherché : {MODELE}). "
            "Entraînez-le avec python src/train.py "
            "ou définissez SENTIMENT_MODELE."
        )
    return joblib.load(MODELE)


def predict(texte: str) -> Prediction:
    """Renvoie l'étiquette et la confiance brute du modèle."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    pipeline = charger_modele()
    etiquette = pipeline.predict([texte])[0]
    score = float(pipeline.predict_proba([texte]).max())
    return {"label": etiquette, "score": round(score, 4)}
