# Semaine 5 : l'interface, notes individuelles

> Trois questions, quelques phrases chacune. Répondez avec ce que vous avez observé.

## 1. Pourquoi l'interface n'importe-t-elle jamais `predict()` ni le fichier `.joblib` ?

L'interface est un client HTTP : elle envoie les avis à l'API et n'embarque ni le code de prédiction ni le fichier du modèle. Le prétraitement, le seuil et le chargement restent au même endroit côté API ; on peut remplacer ou réentraîner le modèle sans modifier la page.

## 2. Que montre l'interface quand le modèle hésite, et pourquoi est-ce mieux qu'un verdict forcé ?

Quand la confiance est sous le seuil de 0,60, la page affiche « Je ne sais pas : à faire vérifier par un humain », la confiance et un message d'abstention. Cela évite de présenter comme certain un verdict que le modèle ne peut pas soutenir.

## 3. Que voit l'utilisateur quand l'API tombe ? Et le fichier `data/avis_exemple.csv` : combien d'avis partent vers un humain ?

Si l'API ne répond plus, l'état de santé et l'analyse affichent « API injoignable : lancez d'abord uvicorn api.main:app ». Le fichier exemple contient six avis : le résumé obtenu est de trois positifs, deux négatifs et un indéterminé, donc un avis à faire vérifier par un humain.
