# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Signaler au pharmacien les ordonnances auxquelles il manque un champ obligatoire, afin qu'il puisse les vérifier avant leur traitement.

## Utilisateur final (obligatoire)

Le pharmacien ou le préparateur qui contrôle l'ordonnance au comptoir. Le système l'aide au contrôle sans se substituer à sa décision professionnelle.

## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

Les champs requis et les règles de contrôle sont définis par les procédures applicables : des règles métier donnent un résultat traçable et vérifiable par champ (b). Il n'est pas nécessaire de disposer d'un jeu d'ordonnances étiquetées (a), et un contrôle local peu coûteux est adapté au traitement de chaque ordonnance (c). Comme une validation à tort peut retarder ou compromettre une prise en charge (d), toute ordonnance signalée ou incertaine reste soumise au pharmacien.

## Données nécessaires et leur origine (obligatoire)

Une image ou une saisie des champs de l'ordonnance, les règles validées par les autorités et procédures professionnelles compétentes, et éventuellement les référentiels nécessaires au contrôle. Les données de santé ne sont accessibles qu'au personnel autorisé et ne sont conservées que si cela est nécessaire et permis.

## Métrique de succès et seuil d'acceptation (obligatoire)

Sur un jeu de cas de test vérifiés par des pharmaciens, mesurer le rappel des ordonnances réellement incomplètes et le taux de champs obligatoires correctement extraits. Seuil pilote proposé : rappel d'au moins 99 % pour les champs bloquants, avec revue humaine systématique avant toute validation définitive.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une ordonnance incomplète acceptée automatiquement peut entraîner un risque clinique ou réglementaire ; une alerte injustifiée peut retarder la délivrance. Le pharmacien examine les champs extraits, confirme ou corrige le résultat et décide de la suite.

## Risques éthiques ou de confidentialité (obligatoire)

Les ordonnances contiennent des données de santé et des identifiants : accès limité, chiffrement, durée de conservation minimale et absence d'envoi à un service externe non autorisé. Les performances doivent aussi être vérifiées sur différents formats et qualités d'image pour éviter des erreurs inégales.

## Approche écartée et pourquoi (facultatif)

Un modèle génératif seul n'est pas retenu pour décider qu'une ordonnance est valide : ses réponses peuvent varier et ne garantissent pas l'application constante de règles réglementaires. La reconnaissance de texte peut être ajoutée comme aide, avec confirmation humaine des champs lus.
