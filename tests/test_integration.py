"""Tests d'intégration du démarrage et des pannes de l'API (TP4, étape D)."""
from pathlib import Path

import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


def test_demarrage_reel_charge_le_modele():
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_demarrage_refuse_si_modele_absent(monkeypatch, tmp_path):
    from fastapi.testclient import TestClient

    import predict
    from api.main import app

    monkeypatch.setattr(predict, "MODELE", tmp_path / "absent.joblib")
    predict.charger_modele.cache_clear()
    with pytest.raises(FileNotFoundError, match="models/sentiment.joblib absent"):
        with TestClient(app):
            pass
    predict.charger_modele.cache_clear()


def test_demarrage_refuse_des_classes_inattendues(monkeypatch):
    import api.model as modele_api

    class ModeleInattendu:
        classes_ = ["negative", "neutral", "positive"]

    monkeypatch.setattr(modele_api, "charger_modele", lambda: ModeleInattendu())
    with pytest.raises(ValueError, match="Classes du modèle non prises en charge"):
        modele_api.SentimentClassifier()


def test_modele_non_charge_renvoie_503(monkeypatch):
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        monkeypatch.delattr(app.state, "classifier", raising=False)
        assert client.get("/health").status_code == 503
        assert client.post("/predict", json={"text": "Avis valide"}).status_code == 503


@pytest.mark.parametrize("erreur", [RuntimeError("panne"), ValueError("bug interne")])
def test_panne_modele_est_masquee_en_500(monkeypatch, erreur):
    from fastapi.testclient import TestClient

    from api.main import app

    class ModeleEnPanne:
        def predict(self, text: str):
            raise erreur

    with TestClient(app) as client:
        monkeypatch.setattr(app.state, "classifier", ModeleEnPanne())
        reponse = client.post("/predict", json={"text": "Avis valide"})
    assert reponse.status_code == 500
    assert reponse.json()["detail"] == "Erreur interne du serveur"
    assert "bug interne" not in reponse.text
