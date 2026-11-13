"""Compatibilité avec les imports et la commande historique du TP2."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sentiment_app import predict as _module  # noqa: E402

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage : python src/predict.py "texte à analyser"')
        raise SystemExit(2)
    try:
        result = _module.predict(" ".join(sys.argv[1:]))
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
    print(f"{result['label']} (confiance {result['score']:.0%})")
else:
    sys.modules[__name__] = _module
