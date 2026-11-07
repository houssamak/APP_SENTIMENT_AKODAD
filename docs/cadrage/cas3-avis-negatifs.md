# Fiche de cadrage : Priorisation des avis négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Classer les avis clients pour faire remonter rapidement à l'équipe les avis négatifs qui nécessitent une réponse ou une action.

## Utilisateur final (obligatoire)

Les agents du service client et les responsables e-commerce, qui consultent une file de priorités puis décident de la réponse à apporter.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

Les milliers d'avis constituent un volume suffisant pour constituer et étiqueter un échantillon représentatif (a), puis entraîner un classifieur de sentiment. Un modèle léger a un coût faible par avis (c) et ses résultats se mesurent sur un jeu de test annoté (b). Un avis négatif manqué peut retarder la résolution d'un problème, mais la décision finale et la réponse restent humaines (d).

## Données nécessaires et leur origine (obligatoire)

Avis publiés ou reçus par le site, avec le texte et une étiquette de sentiment attribuée ou vérifiée par des annotateurs. Supprimer les identifiants personnels, séparer les données d'entraînement et de test, et documenter les règles d'annotation.

## Métrique de succès et seuil d'acceptation (obligatoire)

Mesurer le rappel et la précision de la classe « négatif » sur un jeu de test tenu à l'écart, ainsi que le F1 macro. Seuil pilote proposé : rappel d'au moins 90 % des avis négatifs et F1 macro d'au moins 0,85 ; les résultats doivent être contrôlés par catégorie de produit et de langue.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Un avis négatif mal classé peut rester sans réponse assez longtemps ; un avis positif signalé par erreur mobilise inutilement un agent. Les agents examinent la file triée, peuvent corriger les étiquettes et gardent la responsabilité des réponses publiques.

## Risques éthiques ou de confidentialité (obligatoire)

Les avis peuvent contenir des noms, coordonnées ou informations sensibles : les retirer ou les masquer avant l'analyse et limiter l'accès aux données. Vérifier que les formulations, langues et catégories de produits sont représentées afin que certaines clientèles ne soient pas systématiquement moins bien classées.

## Approche écartée et pourquoi (facultatif)

Des règles fondées uniquement sur des mots négatifs manqueraient les nuances, l'ironie et les formulations indirectes. Un modèle génératif par avis coûterait davantage à grande échelle sans être nécessaire pour une classification à deux classes.
