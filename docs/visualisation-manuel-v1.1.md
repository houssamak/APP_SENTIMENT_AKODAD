# Manuel V1.1 — TP3 : interface et visualisations

L'interface Streamlit utilise les routes `/v1`, envoie la clé `API_KEY` chargée depuis
`.env` et traduit les codes d'erreur stables en messages lisibles. L'onglet CSV présente le
tableau, le compte par verdict, deux graphiques et l'export.

Sur `data/avis_exemple.csv`, les six avis donnent 3 positifs, 2 négatifs et 1
`INDETERMINE`. Les confiances sont réparties dans les tranches `[0,5–0,6[` : 1,
`[0,6–0,7[` : 1, `[0,7–0,8[` : 3, `[0,8–0,9[` : 1 et `[0,9–1]` : 0. Le seul avis
sous 0,60 est envoyé à un humain. Ces graphiques décrivent les sorties du modèle, pas sa
justesse.

## Lancement local

Terminal 1, à la racine du dépôt :

```powershell
.venv\Scripts\python.exe -m uvicorn api.main:app --reload
```

Terminal 2 :

```powershell
.venv\Scripts\python.exe -m streamlit run ui/app.py
```

Le fichier `.env` local contient les clés générées pour les rôles client et admin; il est
ignoré par Git. L'interface Streamlit utilise la clé client côté serveur.
