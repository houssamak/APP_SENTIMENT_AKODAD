# Fiche modèle — Analyse de sentiment des avis

## 1. Identité

- Projet : `sentiment-app`, version du paquet `1.0.0`.
- Modèle : pipeline TF-IDF et régression logistique, entraîné par `src/train.py`.
- Artefact d'entraînement : `models/sentiment.joblib`; copié dans `src/sentiment_app/modele/`
  pendant la construction et inclus dans la roue, mais jamais versionné dans Git.

## 2. Usage prévu

Classer des avis clients rédigés en français comme positifs ou négatifs. Le seuil
d'abstention de l'application renvoie `INDETERMINE` quand le score maximal est inférieur
à 0,60.

## 3. Usages exclus

Le modèle n'est pas destiné aux décisions automatisées concernant des personnes, à la
modération sans revue, aux textes non français, ni à l'interprétation d'opinions nuancées
ou de domaines éloignés des avis clients.

## 4. Données d'entraînement

La dernière mesure versionnée dans `models/metrics.json` indique la source `demo` : 290
avis au total, 232 pour l'entraînement et 58 pour le test. La séparation est stratifiée,
avec la graine 42. Le jeu de démonstration est petit et ne représente pas nécessairement
la diversité des avis réels.

## 5. Performances mesurées

Sur ce jeu de test : F1 macro `0,879`, exactitude `0,8793`, rappel de la classe négative
`0,931`. Ces mesures viennent de `models/metrics.json`; elles ne garantissent pas les
performances sur de nouvelles populations ou d'autres domaines.

## 6. Limites connues

TF-IDF et la régression logistique s'appuient surtout sur les termes appris. La négation,
l'ironie, le sarcasme, le vocabulaire rare et les avis mixtes peuvent conduire à une
classification erronée. Le score est une confiance de modèle, pas une probabilité
calibrée.

## 7. Biais mesurés

Aucune analyse par sous-groupe démographique ou variété linguistique n'a été réalisée.
Des biais de couverture et de vocabulaire sont possibles dans les données de démonstration.

## 8. Explicabilité

Le pipeline utilise une représentation TF-IDF suivie d'une régression logistique. Il est
possible d'inspecter les coefficients et les termes du modèle, mais l'application ne
fournit pas d'explication pour chaque prédiction.

## 9. Conditions d'usage

Utiliser les résultats comme aide au tri. Une personne doit examiner les avis `INDETERMINE`
et toute décision importante. Pour une roue installée hors du dépôt, fournir le chemin du
modèle avec `SENTIMENT_MODELE`; utiliser le scikit-learn de la série 1.5 qui a servi à
l'entraînement.

## 10. Maintenance

Après chaque réentraînement, mettre à jour les métriques, vérifier le jeu de test et les
cas difficiles, puis réviser cette fiche avant de distribuer le nouvel artefact. Garder
ensemble la version scikit-learn et le modèle sérialisé.
