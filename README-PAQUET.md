# sentiment-app

Paquet Python de classification de sentiment d'avis clients rédigés en français. La roue
embarque le pipeline TF-IDF/régression logistique entraîné par le projet et fournit une
fonction Python `sentiment_app.predict` ainsi qu'une commande `sentiment`.

## Installation

```bash
python -m pip install sentiment_app-1.0.0-py3-none-any.whl
```

## Exemples

```python
from sentiment_app import predict

print(predict("Livraison rapide, produit conforme, très satisfait"))
```

```bash
sentiment "Livraison rapide, produit conforme, très satisfait"
sentiment --json "Produit cassé et service injoignable, à fuir"
sentiment --version
```

## Limites

Ce modèle de démonstration a été évalué sur un petit jeu généré; ses scores ne garantissent
pas ses performances sur d'autres domaines. Les scores ne sont pas calibrés. La négation,
l'ironie et les avis mixtes restent difficiles; les décisions importantes nécessitent une
revue humaine. Voir `docs/fiche-modele.md` dans le dépôt source.
