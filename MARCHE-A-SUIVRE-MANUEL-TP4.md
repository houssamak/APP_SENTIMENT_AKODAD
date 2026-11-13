# Manuel V1.1 — TP4 : paquet installable vérifié

Le TP4 du manuel V1.1 correspond au packaging `1.0.0` avec le modèle embarqué. Il ne faut
pas le confondre avec les anciens guides qui appelaient TP4 les tests de qualité.

## Construire

À la racine du dépôt, environnement virtuel activé :

```powershell
python -m pip install -r requirements-dev.txt
python -m pip install -e .
python src/make_demo.py
python src/train.py
Copy-Item models\sentiment.joblib src\sentiment_app\modele\sentiment.joblib -Force
python -m pytest -q
ruff check .
mypy api
node --test web/client.test.mjs
```

Le modèle copié sous `src/sentiment_app/modele/` est exclu de Git et inclus dans la roue.
Ne jamais commiter le modèle binaire.

## Versionner et fabriquer les distributions

Après validation du code, enregistrer un commit, puis poser le tag `v1.0.0` sur ce commit.
Vider `dist/` et `build/`, puis lancer :

```powershell
python -m build
python -m zipfile -l dist\sentiment_app-1.0.0-py3-none-any.whl
python scripts/verifier_livrable.py
```

Le vérificateur exige une roue et une archive source, vérifie leur contenu et le tag, installe
la roue dans un nouvel environnement virtuel hors du dépôt, exécute les six tests du paquet,
puis vérifie la commande installée. Le bilan attendu est `CONFORME`, écrit dans
`docs/livrable-tp4.txt`; ce rapport est ignoré par Git et destiné à accompagner la release.

La publication GitHub n'est pas effectuée dans cette étape : le dépôt distant sera créé et
poussé à la fin des TPs, comme convenu. À ce moment-là, joindre à la release `v1.0.0` la roue,
l'archive source et le rapport `CONFORME`.
