# Journal des versions

## [1.0.0] - 2026-11-13

- Paquet `sentiment-app` installable avec le modèle embarqué dans la roue.
- Ajout de la commande `sentiment` et de la fonction publique `sentiment_app.predict`.
- Vérification de la roue installée dans un environnement isolé.
- Limites connues : jeu de démonstration restreint; négation, ironie et avis mixtes difficiles.

## 0.6.0

- Ajout du paquet installable `sentiment-app` et de la commande `sentiment`.
- Ajout des commandes `predict`, `serve`, `ui` et `--version`.
- Configuration du modèle par `SENTIMENT_MODELE`.
- L'API importe maintenant `sentiment_app.predict` directement.
- La roue inclut le code de l'application, sans tests, données ni modèle.
- Dépendances runtime déclarées; scikit-learn est limité à la série 1.5.

## 0.5.0

- Ajout de l'interface Streamlit et de l'analyse de fichiers CSV.

## 0.4.0

- Renforcement des tests, du contrôle qualité et de la gestion de l'abstention.

## 0.3.0

- Ajout de l'API FastAPI.

## 0.2.0

- Entraînement et évaluation du modèle de sentiment.

## 0.1.0

- Cadrage du projet et mise en place de l'environnement.
