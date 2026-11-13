# TP6 — Packager l'application

Le projet est distribuable sous forme de roue Python `sentiment_app-0.6.0-py3-none-any.whl`.
La version est définie une seule fois dans `sentiment_app.__version__`; setuptools la lit
depuis `pyproject.toml` et la commande `sentiment --version` l'affiche.

## Installer en développement

```powershell
pip install -e ".[ui]"
sentiment --version
sentiment predict "Livraison rapide, produit conforme, très satisfait"
sentiment serve
# Dans un autre terminal, avec l'API démarrée :
sentiment ui
```

Pour installer les seules dépendances de l'API, utiliser `pip install -e .`. Le supplément
`[ui]` installe Streamlit, pandas et requests.

## Construire et vérifier la roue

```powershell
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
python -m build --wheel
python -m venv $env:TEMP\roue-tp6
$env:TEMP\roue-tp6\Scripts\pip install dist\sentiment_app-0.6.0-py3-none-any.whl
$env:SENTIMENT_MODELE = (Resolve-Path models\sentiment.joblib).Path
$env:TEMP\roue-tp6\Scripts\sentiment predict "Livraison rapide, produit conforme, très satisfait"
Remove-Item Env:SENTIMENT_MODELE
```

Lancer la commande depuis `$env:TEMP` permet de vérifier que la roue ne dépend pas du
répertoire du dépôt. Le modèle n'est pas inclus : en dehors du dépôt, définir
`SENTIMENT_MODELE` vers un fichier joblib produit avec scikit-learn 1.5.x. Le paquet
déclare `scikit-learn>=1.5,<1.6` afin de conserver la compatibilité du modèle sérialisé.

## Contenu et publication

La roue comprend `sentiment_app`, `api`, `ui` et les métadonnées. Elle exclut les tests,
les jeux de données, les modèles et les scripts d'entraînement. `dist/` et `*.egg-info/`
sont ignorés par Git. La CI construit et installe la roue depuis `/tmp`, puis effectue une
prédiction avec un chemin de modèle explicite.

Après revue locale, le jalon de version se crée avec :

```bash
git add -A
git commit -m "Semaine 6 : paquet installable, version 0.6.0"
git tag -a v0.6.0 -m "TP6 : paquet installable"
```

Le dépôt distant sera configuré et poussé à la fin des TPs, comme prévu.
