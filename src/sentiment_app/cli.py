"""Commande installée « sentiment »."""

import argparse
import json
import sys

from sentiment_app import __version__, predict


def main(argv: list[str] | None = None) -> int:
    """Classe un avis, avec sortie texte ou JSON."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    # Compatibilité avec l'interface `sentiment predict ...` du jalon 0.6.0.
    if arguments and arguments[0] == "predict":
        arguments.pop(0)
    parser = argparse.ArgumentParser(
        prog="sentiment", description="Classe le sentiment d'un avis en français."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--json", action="store_true", help="produire une sortie JSON")
    parser.add_argument("texte", nargs="+", help="l'avis à classer")
    args = parser.parse_args(arguments)

    try:
        resultat = predict(" ".join(args.texte))
    except (FileNotFoundError, ValueError) as exc:
        print(f"erreur : {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(resultat, ensure_ascii=False))
    else:
        print(f"{resultat['label']} (confiance {resultat['score']:.0%})")
    return 0
