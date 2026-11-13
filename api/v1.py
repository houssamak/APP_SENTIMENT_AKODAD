"""Routes versionnées, protégées par clé d'API."""

import json
import logging
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request

from api.model import SEUIL_ABSTENTION, SentimentClassifier, SentimentResult
from api.schemas import ErreurV1, HealthResponse, ModeleInfo, PredictRequest, PredictResponse
from api.securite import Role, exiger

logger = logging.getLogger("sentiment_api")
RACINE = Path(__file__).resolve().parents[1]
ERREURS: dict[int | str, dict[str, Any]] = {
    code: {"model": ErreurV1} for code in (401, 403, 422, 500, 503)
}
router = APIRouter(prefix="/v1", tags=["v1"], responses=ERREURS)


def classifier(request: Request) -> SentimentClassifier:
    clf = getattr(request.app.state, "classifier", None)
    if clf is None:
        raise HTTPException(503, "Modèle non chargé")
    return clf


Classifier = Annotated[SentimentClassifier, Depends(classifier)]


@router.get("/health", response_model=HealthResponse, summary="Santé (public)")
def sante(clf: Classifier) -> dict[str, str]:
    return {"status": "OK", "model": clf.model_name}


@router.post("/predict", response_model=PredictResponse, summary="Classer un avis")
def predire(
    corps: PredictRequest,
    clf: Classifier,
    _role: Annotated[Role, Depends(exiger("client", "admin"))],
) -> SentimentResult:
    try:
        resultat = clf.predict(corps.text)
    except Exception:
        logger.exception("Erreur interne lors de la prédiction")
        raise HTTPException(500, "Erreur interne du serveur") from None
    logger.info("v1 predict -> %s (%.2f)", resultat["label"], resultat["score"])
    return resultat


@router.get("/modele", response_model=ModeleInfo, summary="Métriques (admin)")
def informations_modele(
    request: Request,
    _role: Annotated[Role, Depends(exiger("admin"))],
) -> ModeleInfo:
    clf = classifier(request)
    chemin = RACINE / "models" / "metrics.json"
    try:
        metriques = json.loads(chemin.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        metriques = {}
    return ModeleInfo(
        model=clf.model_name,
        seuil_abstention=SEUIL_ABSTENTION,
        metriques=metriques,
    )
