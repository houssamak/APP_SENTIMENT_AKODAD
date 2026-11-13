#!/usr/bin/env python
"""Vérifie le paquet 1.0.0 depuis une installation réellement isolée."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import venv
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
DIST = RACINE / "dist"
VERSION = "1.0.0"
ROUE_NOM = f"sentiment_app-{VERSION}-py3-none-any.whl"
SOURCE_NOM = f"sentiment_app-{VERSION}.tar.gz"


def lancer(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    resultat = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    if resultat.returncode:
        raise RuntimeError(
            f"Commande échouée ({resultat.returncode}) : {' '.join(command)}\n"
            f"{resultat.stdout[-2500:]}\n{resultat.stderr[-2500:]}"
        )
    return resultat.stdout.strip()


def verifier_tag() -> None:
    head = lancer(["git", "rev-parse", "HEAD"], cwd=RACINE)
    cible = lancer(["git", "rev-parse", "v1.0.0^{}"], cwd=RACINE)
    if head != cible:
        raise RuntimeError("L'étiquette v1.0.0 ne pointe pas sur le dernier commit.")


def verifier_roue(roue: Path) -> None:
    with zipfile.ZipFile(roue) as archive:
        noms = set(archive.namelist())
        requis = {
            "sentiment_app/__init__.py",
            "sentiment_app/cli.py",
            "sentiment_app/predict.py",
            "sentiment_app/modele/sentiment.joblib",
            "sentiment_app-1.0.0.dist-info/METADATA",
            "sentiment_app-1.0.0.dist-info/entry_points.txt",
        }
        if missing := requis - noms:
            raise RuntimeError(f"Fichiers manquants dans la roue : {sorted(missing)}")
        interdits = ("tests/", "api/", "ui/", "data/", "models/", "src/")
        if found := sorted(nom for nom in noms if nom.startswith(interdits)):
            raise RuntimeError(f"Fichiers hors paquet inclus dans la roue : {found}")
        metadata = archive.read("sentiment_app-1.0.0.dist-info/METADATA").decode("utf-8")
        if "Version: 1.0.0" not in metadata or "Requires-Dist: scikit-learn==1.5.*" not in metadata:
            raise RuntimeError("Version ou dépendance scikit-learn absente des métadonnées.")
        entrypoints = archive.read(
            "sentiment_app-1.0.0.dist-info/entry_points.txt"
        ).decode("utf-8")
        if "sentiment = sentiment_app.cli:main" not in entrypoints:
            raise RuntimeError("Point d'entrée `sentiment` absent de la roue.")


def verifier_installation(roue: Path) -> tuple[str, str]:
    with tempfile.TemporaryDirectory(prefix="sentiment-livrable-") as repertoire:
        temporaire = Path(repertoire)
        environnement_virtuel = temporaire / ".venv"
        venv.EnvBuilder(with_pip=True).create(environnement_virtuel)
        binaires = environnement_virtuel / ("Scripts" if os.name == "nt" else "bin")
        python = binaires / ("python.exe" if os.name == "nt" else "python")
        commande = binaires / ("sentiment.exe" if os.name == "nt" else "sentiment")

        lancer([str(python), "-m", "pip", "install", str(roue), "pytest>=8"], cwd=temporaire)
        shutil.copy2(RACINE / "tests" / "test_paquet.py", temporaire / "test_paquet.py")
        environnement = os.environ.copy()
        environnement["VERIFICATION_LIVRABLE"] = "1"
        environnement.pop("SENTIMENT_MODELE", None)
        tests = lancer(
            [str(python), "-m", "pytest", "-q", "test_paquet.py"],
            cwd=temporaire,
            env=environnement,
        )
        prediction = lancer(
            [str(commande), "--json", "Produit cassé et service injoignable, à fuir"],
            cwd=temporaire,
            env=environnement,
        )
        return tests, prediction


def main() -> int:
    resultats: list[str] = []
    try:
        if not DIST.is_dir():
            raise RuntimeError("dist/ absent : construisez d'abord les distributions.")
        attendu = {ROUE_NOM, SOURCE_NOM}
        presents = {f.name for f in DIST.iterdir() if f.is_file()}
        if presents != attendu:
            raise RuntimeError(f"dist/ doit contenir exactement {sorted(attendu)}, reçu {sorted(presents)}")
        resultats.append(f"[OK] roue présente : {ROUE_NOM}")
        resultats.append(f"[OK] distribution source présente : {SOURCE_NOM}")
        verifier_roue(DIST / ROUE_NOM)
        resultats.append("[OK] modèle embarqué, point d'entrée et dépendances vérifiés; aucun test ni donnée dans la roue")
        changelog = (RACINE / "CHANGELOG.md").read_text(encoding="utf-8")
        if "[1.0.0]" not in changelog:
            raise RuntimeError("CHANGELOG.md ne décrit pas la version [1.0.0].")
        resultats.append("[OK] CHANGELOG.md décrit la version [1.0.0]")
        verifier_tag()
        resultats.append("[OK] tag v1.0.0 posé sur le dernier commit")
        tests, prediction = verifier_installation(DIST / ROUE_NOM)
        resultats.append("[OK] installation de la roue dans un environnement neuf")
        resultats.append(f"[OK] tests du paquet installé : {tests}")
        resultats.append(f"[OK] commande installée : {prediction}")
        resultats.append("Bilan : CONFORME")
    except (OSError, RuntimeError, subprocess.SubprocessError, zipfile.BadZipFile) as exc:
        resultats.append(f"[ÉCHEC] {exc}")
        resultats.append("Bilan : NON CONFORME")

    rapport = "\n".join(resultats) + "\n"
    chemin_rapport = RACINE / "docs" / "livrable-tp4.txt"
    chemin_rapport.write_text(rapport, encoding="utf-8")
    print(rapport, end="")
    print(f"Rapport : {chemin_rapport.relative_to(RACINE)}")
    return 0 if "Bilan : CONFORME" in rapport else 1


if __name__ == "__main__":
    raise SystemExit(main())
