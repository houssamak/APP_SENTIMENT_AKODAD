# Semaine 3 : l'API, notes individuelles

> Deux questions, quelques phrases chacune. Répondez avec ce que vous avez observé, pas avec le cours.

## 1. Pourquoi l'API refuse-t-elle de démarrer sans `models/sentiment.joblib`, plutôt que de démarrer et de répondre 503 ?

Au démarrage, FastAPI exécute le `lifespan`, qui construit le classifieur et charge `models/sentiment.joblib` une fois. Si le fichier manque, `charger_modele()` lève `FileNotFoundError` et le démarrage échoue : le service ne se déclare pas prêt alors qu'il ne peut pas répondre. Le 503 de `_classifier()` couvre plutôt le cas où l'application tourne sans classifieur dans son état.

## 2. Un texte vide est refusé deux fois : par Pydantic, puis par `predict()`. Est-ce redondant ?

La validation Pydantic rejette un texte vide à la frontière HTTP et renvoie 422 avant l'appel à la route. `predict()` garde aussi son propre contrôle pour les appels directs depuis le script ou d'autres composants qui ne passent pas par l'API. Les deux protections sont donc utiles à des niveaux différents.
