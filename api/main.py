"""API REST du classifieur de sentiment, avec compatibilité historique et /v1."""

import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.model import load_model
from api.schemas import ErrorResponse, HealthResponse, PredictRequest, PredictResponse
from api.securite import charger_cles
from api.v1 import router as v1_router

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("sentiment_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Valide la configuration et charge le modèle avant la première requête."""
    app.state.api_keys = charger_cles()
    logger.info("Démarrage de l'API avec %d clé(s) d'API", len(app.state.api_keys))
    app.state.classifier = load_model()
    logger.info("Modèle chargé avec succès : %s", app.state.classifier.model_name)
    yield
    logger.info("Arrêt de l'API")


app = FastAPI(
    title="Sentiment Analysis API",
    description="API de classification de sentiment en français, versionnée sous /v1.",
    version="1.0.0",
    lifespan=lifespan,
)

origines = [
    origine.strip()
    for origine in os.environ.get(
        "CORS_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500"
    ).split(",")
    if origine.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origines,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)


def _champs_validation(exc: RequestValidationError) -> list[dict[str, str]]:
    return [
        {
            "champ": ".".join(str(part) for part in erreur.get("loc", ())),
            "message": str(erreur.get("msg", "Entrée invalide")),
        }
        for erreur in exc.errors()
    ]


@app.exception_handler(RequestValidationError)
async def erreur_validation(request: Request, exc: RequestValidationError) -> JSONResponse:
    if request.url.path.startswith("/v1/"):
        return JSONResponse(
            status_code=422,
            content={
                "erreur": {
                    "code": "ENTREE_INVALIDE",
                    "message": "Entrée refusée par le contrat de l'API",
                    "champs": _champs_validation(exc),
                }
            },
        )
    return JSONResponse(status_code=422, content={"detail": jsonable_encoder(exc.errors())})


@app.exception_handler(StarletteHTTPException)
async def erreur_http(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    if request.url.path.startswith("/v1/"):
        code = {
            401: "NON_AUTHENTIFIE",
            403: "ACCES_REFUSE",
            422: "ENTREE_INVALIDE",
            500: "ERREUR_INTERNE",
            503: "MODELE_INDISPONIBLE",
        }.get(exc.status_code, "ERREUR_HTTP")
        message = str(exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={"erreur": {"code": code, "message": message, "champs": []}},
            headers=exc.headers,
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )


app.include_router(v1_router)


@app.get("/", summary="Accueil")
async def root() -> dict[str, str]:
    return {"message": "Sentiment Analysis API", "docs": "/docs", "health": "/health"}


@app.get("/health", response_model=HealthResponse, summary="Santé historique")
async def health_check() -> dict[str, str]:
    clf = getattr(app.state, "classifier", None)
    if clf is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    return {"status": "OK", "model": clf.model_name}


@app.post(
    "/predict",
    response_model=PredictResponse,
    deprecated=True,
    summary="Classifier un texte (route historique, utiliser /v1/predict)",
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def predict(request: PredictRequest) -> JSONResponse:
    clf = getattr(app.state, "classifier", None)
    if clf is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    try:
        result = clf.predict(request.text)
    except Exception:
        logger.exception("Erreur lors de la prédiction historique")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur") from None
    logger.info("legacy predict -> %s (%.2f)", result["label"], result["score"])
    return JSONResponse(
        content=result,
        headers={"Deprecation": "true", "Link": '</v1/predict>; rel="successor-version"'},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, log_level="info")
