"""Tests exécutés contre la distribution installée, depuis un dossier isolé."""

import json
import os
import shutil
import subprocess
import sys
from importlib.resources import files
from pathlib import Path

import pytest

if os.environ.get("VERIFICATION_LIVRABLE") != "1":
    pytest.skip(
        "ces tests ciblent le paquet installé; lancez python scripts/verifier_livrable.py",
        allow_module_level=True,
    )

from sentiment_app import __version__, predict


def test_version_installee() -> None:
    assert __version__ == "1.0.0"


def test_modele_embarque_dans_le_paquet() -> None:
    assert files("sentiment_app").joinpath("modele/sentiment.joblib").is_file()


def test_prediction_positive_depuis_le_modele_empaquete(monkeypatch) -> None:
    monkeypatch.delenv("SENTIMENT_MODELE", raising=False)
    resultat = predict("Livraison rapide, produit conforme, très satisfait")
    assert resultat["label"] == "positive"
    assert resultat["score"] == pytest.approx(0.777, abs=0.01)


def test_prediction_negative_depuis_le_modele_empaquete(monkeypatch) -> None:
    monkeypatch.delenv("SENTIMENT_MODELE", raising=False)
    resultat = predict("Produit cassé et service injoignable, à fuir")
    assert resultat["label"] == "negative"


def test_texte_vide_refuse() -> None:
    with pytest.raises(ValueError, match="texte vide"):
        predict("   ")


def test_commande_installee_produit_du_json(monkeypatch) -> None:
    monkeypatch.delenv("SENTIMENT_MODELE", raising=False)
    dossier_binaires = str(Path(sys.executable).parent)
    commande = shutil.which("sentiment", path=dossier_binaires)
    assert commande is not None
    environnement = os.environ.copy()
    environnement.pop("SENTIMENT_MODELE", None)
    resultat = subprocess.run(
        [commande, "--json", "Produit cassé et service injoignable, à fuir"],
        capture_output=True,
        text=True,
        check=True,
        env=environnement,
    )
    assert json.loads(resultat.stdout)["label"] == "negative"
