"""Interface en ligne de commande de l'application."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from sentiment_app import __version__


def main() -> int:
    parser = argparse.ArgumentParser(prog="sentiment")
    parser.add_argument("--version", action="version", version=f"sentiment-app {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    predict_parser = commands.add_parser("predict", help="classer un avis")
    predict_parser.add_argument("text", nargs="+", help="texte à analyser")
    commands.add_parser("serve", help="démarrer l'API FastAPI")
    commands.add_parser("ui", help="démarrer l'interface Streamlit")
    args = parser.parse_args()

    if args.command == "predict":
        try:
            from api.model import load_model

            result = load_model().predict(" ".join(args.text))
        except (FileNotFoundError, ValueError) as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(json.dumps(result, ensure_ascii=False))
        return 0

    if args.command == "serve":
        import uvicorn

        uvicorn.run("api.main:app", host="0.0.0.0", port=8000)
        return 0

    app_path = Path(__file__).resolve().parents[1] / "ui" / "app.py"
    return subprocess.call([sys.executable, "-m", "streamlit", "run", str(app_path)])
