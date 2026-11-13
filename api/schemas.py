"""Contrats d'entrée et de sortie de l'API (Pydantic v2)."""
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class PredictRequest(BaseModel):
    """Requête de prédiction."""
    text: str = Field(..., min_length=1, max_length=2000, description="Texte à classifier",
                      examples=["Livraison rapide, produit conforme, très satisfait"])

    @field_validator("text")
    @classmethod
    def refuser_texte_blanc(cls, valeur: str) -> str:
        if not valeur.strip():
            raise ValueError("Le texte ne peut pas être vide ou composé d'espaces")
        return valeur


class PredictResponse(BaseModel):
    """Réponse de prédiction."""
    label: Literal["POSITIVE", "NEGATIVE", "INDETERMINE"] = Field(
        ..., description="POSITIVE, NEGATIVE ou INDETERMINE"
    )
    score: float = Field(..., ge=0, le=1, description="Confiance de la classe prédite")
    text: str = Field(..., description="Aperçu du texte analysé (100 caractères)")


Label = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]


class ChampInvalide(BaseModel):
    champ: str
    message: str


class DetailErreur(BaseModel):
    code: str
    message: str
    champs: list[ChampInvalide] = Field(default_factory=list)


class ErreurV1(BaseModel):
    """Format stable des erreurs de l'API versionnée."""

    erreur: DetailErreur


class ModeleInfo(BaseModel):
    model: str
    seuil_abstention: float
    metriques: dict[str, float | int | str]


class HealthResponse(BaseModel):
    """Réponse de l'endpoint de santé."""
    status: str = Field(..., description="OK si le modèle est chargé")
    model: str = Field(..., description="Nom du modèle servi")


class ErrorResponse(BaseModel):
    """Format standard des erreurs FastAPI."""
    detail: str
