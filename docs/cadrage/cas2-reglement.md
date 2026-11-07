# Fiche de cadrage : Questions sur le règlement intérieur

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Aider les élèves, parents et personnels à trouver une réponse fiable à leurs questions sur le règlement intérieur de l'école.

## Utilisateur final (obligatoire)

Les élèves, parents et personnels administratifs qui cherchent à comprendre une règle ou une procédure de l'établissement.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

Les réponses doivent être tirées du règlement et renvoyer à l'article ou à la page source pour être vérifiables (b). Les documents existent déjà, tandis qu'un jeu de questions-réponses étiquetées n'est pas garanti (a) : la recherche dans les documents, suivie d'une formulation, convient mieux qu'un classifieur. Une réponse erronée peut induire une famille en erreur sur ses droits ou obligations (d) ; en l'absence de source pertinente, l'assistant doit s'abstenir et orienter vers l'administration.

## Données nécessaires et leur origine (obligatoire)

Versions officielles et à jour du règlement intérieur, annexes et procédures publiées par l'établissement, avec titres, dates et numéros de page ou d'article. Les éventuelles questions de test sont anonymisées et validées par l'équipe administrative.

## Métrique de succès et seuil d'acceptation (obligatoire)

Sur un jeu de questions représentatif validé par l'administration, mesurer la proportion de réponses exactes appuyées par une citation pertinente ainsi que le taux d'abstention correcte quand les documents ne répondent pas. Seuil pilote proposé : au moins 90 % de réponses correctement sourcées et aucune réponse non sourcée sur les questions de test hors périmètre.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une réponse erronée peut entraîner une démarche manquée ou une mauvaise compréhension d'une règle. L'assistant affiche la source et sa date ; pour les situations individuelles ou ambiguës, il renvoie vers le secrétariat, qui reste l'autorité compétente.

## Risques éthiques ou de confidentialité (obligatoire)

Les questions peuvent révéler des informations sur des élèves, notamment des mineurs : ne pas les réutiliser pour entraîner le système, limiter les journaux et éviter la collecte de données personnelles. Les documents doivent être accessibles sans discrimination et leur version affichée doit rester identifiable.

## Approche écartée et pourquoi (facultatif)

Un modèle génératif seul peut produire une règle plausible mais absente du règlement. Le RAG impose de rechercher une source et permet de s'abstenir quand aucun passage fiable ne répond à la question.
