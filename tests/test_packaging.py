"""Vérifications des métadonnées de distribution et de l'API publique."""

import subprocess
import sys
import tomllib
from importlib import import_module, metadata
from pathlib import Path

import sentiment_app

predict_module = import_module("sentiment_app.predict")

RACINE = Path(__file__).resolve().parents[1]


def test_version_unique_lue_dans_le_paquet() -> None:
    config = tomllib.loads((RACINE / "pyproject.toml").read_text(encoding="utf-8"))
    assert config["project"]["version"] == "1.0.0"
    assert sentiment_app.__version__ == metadata.version("sentiment-app") == "1.0.0"


def test_modele_declare_comme_ressource_du_paquet() -> None:
    config = tomllib.loads((RACINE / "pyproject.toml").read_text(encoding="utf-8"))
    assert config["tool"]["setuptools"]["package-data"]["sentiment_app"] == [
        "modele/*.joblib"
    ]


def test_api_importe_le_paquet_sans_modifier_sys_path() -> None:
    source = (RACINE / "api" / "model.py").read_text(encoding="utf-8")
    assert "from sentiment_app.predict import" in source
    assert "sys.path" not in source


def test_commande_affiche_la_version() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "sentiment_app", "--version"],
        cwd=RACINE,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "sentiment 1.0.0"


def test_paquet_declare_uniquement_code_et_dependances_runtime() -> None:
    config = tomllib.loads((RACINE / "pyproject.toml").read_text(encoding="utf-8"))
    assert config["tool"]["setuptools"]["packages"]["find"]["where"] == ["src"]
    assert "scikit-learn==1.5.*" in config["project"]["dependencies"]
    assert config["project"]["optional-dependencies"]["test"] == ["pytest>=8"]


def test_compatibilite_import_predict_du_tp2() -> None:
    sys.path.insert(0, str(RACINE / "src"))
    try:
        import predict as predict_legacy

        assert predict_legacy is predict_module
    finally:
        sys.path.remove(str(RACINE / "src"))
