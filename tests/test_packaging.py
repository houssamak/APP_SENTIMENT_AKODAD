"""Vérifications du paquet installable du TP6."""

import subprocess
import sys
import tomllib
from pathlib import Path

import sentiment_app
from sentiment_app import predict

RACINE = Path(__file__).resolve().parents[1]


def test_version_unique_lue_dans_le_paquet() -> None:
    config = tomllib.loads((RACINE / "pyproject.toml").read_text(encoding="utf-8"))
    assert sentiment_app.__version__ == "0.6.0"
    assert config["project"]["dynamic"] == ["version"]
    assert config["tool"]["setuptools"]["dynamic"]["version"] == {
        "attr": "sentiment_app.__version__"
    }


def test_chemin_modele_configurable_par_environnement(monkeypatch) -> None:
    chemin = Path("/tmp/modele-test.joblib")
    monkeypatch.setenv("SENTIMENT_MODELE", str(chemin))
    assert predict.chemin_modele() == chemin


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
    assert result.stdout.strip() == "sentiment-app 0.6.0"


def test_paquet_declare_uniquement_code_et_dependances_runtime() -> None:
    config = tomllib.loads((RACINE / "pyproject.toml").read_text(encoding="utf-8"))
    assert config["tool"]["setuptools"]["packages"] == ["sentiment_app", "api", "ui"]
    assert any(dep.startswith("scikit-learn>=1.5,<1.6") for dep in config["project"]["dependencies"])
    assert "streamlit>=1.39,<1.40" in config["project"]["optional-dependencies"]["ui"]


def test_compatibilite_import_predict_du_tp2() -> None:
    sys.path.insert(0, str(RACINE / "src"))
    try:
        import predict as predict_legacy

        assert predict_legacy is predict
    finally:
        sys.path.remove(str(RACINE / "src"))
