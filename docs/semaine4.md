# Semaine 4 : tests approfondis et qualité, notes individuelles

> Résultats des exécutions locales du TP4.

Suite complète après les corrections : **82 passed, 4 xfailed**, sans test en échec. Les quatre `xfail` sont les erreurs du modèle explicitement déclarées dans le jeu d'or.

## 1. Couverture

- Avant (étape A) : 91 %, lignes jamais exécutées : `api/main.py` 49 et 77–79 (API sans modèle chargé et erreur interne) et 85–87 (lancement direct du serveur).
- Après les tests d'intégration (étape D) : 98 % ; seules les lignes du lancement direct de l'API restent hors couverture, car le serveur se lance par la commande `uvicorn`.

## 2. Défauts trouvés

| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| Un texte composé d'espaces Unicode pouvait passer le contrôle de longueur puis échouer plus loin dans le modèle. | Tests paramétrés et propriété Hypothesis couvrant notamment `\x85`. | Validateur Pydantic qui refuse une valeur vide après `strip()`. |
| Une `ValueError` du modèle était présentée comme un 422, avec son message interne. | Test d'intégration d'un modèle défaillant. | Toutes les exceptions internes donnent un 500 générique, sans exposer leur détail. |
| Des avis hors vocabulaire recevaient une étiquette ferme avec une confiance d'environ 0,52. | Essai T24 avec des mots inventés. | Abstention `INDETERMINE` sous le seuil mesuré de 0,60. |

## 3. Seuil d'abstention

- À 0,50 : 58/58 avis traités, exactitude 0,879, 7 erreurs ; à 0,60 : 42/58 traités, exactitude 0,952, 2 erreurs et 16 avis à un humain ; à 0,70 : 37/58 traités, exactitude 1,000, aucun faux verdict et 21 avis à un humain.
- Seuil retenu : 0,60 ; 28 % du jeu de test sont envoyés à un humain. C'est un compromis entre la baisse des erreurs et le volume d'avis que l'équipe doit examiner.

## 4. Jeu d'or

- Bilan sur 20 avis : 6 justes, 10 abstentions et 4 erreurs franches déclarées (`xfail`).
- Le seuil réduit les verdicts hasardeux, mais le jeu d'or révèle que ce modèle simple se trompe encore sur certaines négations, formulations ironiques et expressions indirectes.

## 5. Outils statiques

- Remarques au départ : ruff signalait 11 problèmes de code (imports inutilisés ou mal ordonnés, exceptions, `zip` et noms ambigus) ; mypy ne signalait aucun problème sur les quatre fichiers de l'API.
- Ces outils n'avaient pas détecté les défauts de comportement de l'API. Le typage `TypedDict` et `Literal` rend maintenant les étiquettes explicites ; ruff et mypy passent sans remarque après les corrections.
