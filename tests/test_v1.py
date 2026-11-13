"""Tests du contrat versionné, de l'authentification et des rôles."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from api.securite import charger_cles

CLIENT_KEY = "test-client-key-not-a-secret"
ADMIN_KEY = "test-admin-key-not-a-secret"


@pytest.fixture
def api(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("API_KEYS", f"{CLIENT_KEY}:client,{ADMIN_KEY}:admin")
    from api.main import app

    with TestClient(app) as client:
        yield client


def test_charge_cles_et_roles() -> None:
    assert charger_cles(f"{CLIENT_KEY}:client,{ADMIN_KEY}:admin") == {
        CLIENT_KEY: "client",
        ADMIN_KEY: "admin",
    }


@pytest.mark.parametrize(
    "configuration, attendu",
    [
        ("", "Aucune clé"),
        ("short:client", "clé trop courte"),
        (f"{CLIENT_KEY}:root", "rôle invalide"),
        (f"{CLIENT_KEY}:client,{CLIENT_KEY}:admin", "dupliquée"),
    ],
)
def test_refuse_configuration_de_cles_invalide(configuration: str, attendu: str) -> None:
    with pytest.raises(ValueError, match=attendu) as exc:
        charger_cles(configuration)
    assert CLIENT_KEY not in str(exc.value)


def test_api_refuse_de_demarrer_sans_configuration_valide(monkeypatch: pytest.MonkeyPatch) -> None:
    from api.main import app

    monkeypatch.setenv("API_KEYS", "short:client")
    with pytest.raises(ValueError, match="clé trop courte"):
        with TestClient(app):
            pass


def test_sante_v1_est_publique(api: TestClient) -> None:
    response = api.get("/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"


@pytest.mark.parametrize(
    "headers",
    [{}, {"X-API-Key": "unknown-key-not-a-secret"}],
    ids=["missing", "unknown"],
)
def test_predict_v1_refuse_cles_absentes_ou_inconnues(
    api: TestClient, headers: dict[str, str]
) -> None:
    response = api.post("/v1/predict", json={"text": "Très bon produit"}, headers=headers)
    assert response.status_code == 401
    assert response.json()["erreur"]["code"] == "NON_AUTHENTIFIE"
    assert response.headers["www-authenticate"] == "ApiKey"


@pytest.mark.parametrize("key", [CLIENT_KEY, ADMIN_KEY])
def test_client_et_admin_peuvent_predire(api: TestClient, key: str) -> None:
    response = api.post(
        "/v1/predict", json={"text": "Livraison rapide, produit conforme, très satisfait"},
        headers={"X-API-Key": key},
    )
    assert response.status_code == 200
    assert response.json()["label"] == "POSITIVE"


def test_entree_invalide_a_un_format_stable(api: TestClient) -> None:
    response = api.post(
        "/v1/predict", json={"text": "   "}, headers={"X-API-Key": CLIENT_KEY}
    )
    erreur = response.json()["erreur"]
    assert response.status_code == 422
    assert erreur["code"] == "ENTREE_INVALIDE"
    assert erreur["champs"][0]["champ"] == "body.text"


@pytest.mark.parametrize("body", [{}, {"text": 42}, {"text": "x" * 2001}])
def test_validation_v1_signale_les_champs(api: TestClient, body: dict[str, object]) -> None:
    response = api.post("/v1/predict", json=body, headers={"X-API-Key": CLIENT_KEY})
    assert response.status_code == 422
    assert response.json()["erreur"]["code"] == "ENTREE_INVALIDE"
    assert response.json()["erreur"]["champs"]


def test_route_modele_refuse_le_role_client(api: TestClient) -> None:
    response = api.get("/v1/modele", headers={"X-API-Key": CLIENT_KEY})
    assert response.status_code == 403
    assert response.json()["erreur"]["code"] == "ACCES_REFUSE"


def test_route_modele_admin_fournit_seuil_et_metriques(api: TestClient) -> None:
    response = api.get("/v1/modele", headers={"X-API-Key": ADMIN_KEY})
    body = response.json()
    assert response.status_code == 200
    assert body["seuil_abstention"] == 0.60
    assert body["metriques"]["f1_macro"] == 0.879


def test_route_historique_annonce_son_remplacement(api: TestClient) -> None:
    response = api.post("/predict", json={"text": "Très satisfait"})
    assert response.status_code == 200
    assert response.headers["deprecation"] == "true"
    assert response.headers["link"] == '</v1/predict>; rel="successor-version"'


def test_cors_autorise_le_client_web_local(api: TestClient) -> None:
    response = api.options(
        "/v1/predict",
        headers={
            "Origin": "http://localhost:5500",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,x-api-key",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5500"


def test_panne_modele_est_formatee_sans_detail_interne(api: TestClient, monkeypatch) -> None:
    from api.main import app

    class ModeleEnPanne:
        def predict(self, _texte: str):
            raise RuntimeError("secret interne")

    monkeypatch.setattr(app.state, "classifier", ModeleEnPanne())
    response = api.post(
        "/v1/predict", json={"text": "avis"}, headers={"X-API-Key": CLIENT_KEY}
    )
    assert response.status_code == 500
    assert response.json()["erreur"]["code"] == "ERREUR_INTERNE"
    assert "secret interne" not in response.text


def test_cle_admin_requise_dans_openapi(api: TestClient) -> None:
    schema = api.get("/openapi.json").json()
    assert schema["components"]["securitySchemes"]["APIKeyHeader"]["name"] == "X-API-Key"
    assert schema["paths"]["/v1/predict"]["post"]["security"]
    assert schema["paths"]["/predict"]["post"]["deprecated"] is True
