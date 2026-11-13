# Manuel V1.1 — TP2 : API versionnée et protégée

Cette étape complète l'API historique sans supprimer `/health` et `/predict` : les clients
existants continuent de fonctionner, tandis que les nouveaux utilisent `/v1`.

## Configuration locale

```powershell
Copy-Item .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(24))"
```

Générer deux clés différentes et remplacer les exemples dans `.env` :

```dotenv
API_KEYS=cle-client-generee:client,cle-admin-generee:admin
API_KEY=cle-client-generee
API_URL=http://127.0.0.1:8000
```

Ne jamais commiter `.env`. `API_KEYS` contrôle l'API et `API_KEY` configure les clients.
La route de santé `/v1/health` est publique, `/v1/predict` accepte les rôles `client` et
`admin`, et `/v1/modele` est réservée au rôle `admin`.

## Contrôles effectués

- Authentification : clé absente ou inconnue refusée en 401.
- Autorisation : clé client refusée sur `/v1/modele` en 403; clé admin autorisée.
- Contrat : entrées invalides renvoyées en 422 avec le code stable `ENTREE_INVALIDE` et
  les champs concernés.
- Compatibilité : `/predict` reste disponible et porte `Deprecation: true` ainsi qu'un
  lien vers `/v1/predict`.
- CORS : le client de développement sur `http://localhost:5500` est autorisé; les autres
  origines se configurent avec `CORS_ORIGINS`.
- Client web statique : `web/index.html` et `web/client.js` utilisent les routes `/v1`.

Lancer l'API avec `uvicorn api.main:app --reload`, puis le client web dans un autre terminal
avec `python -m http.server 5500 --directory web`. Les tests du client s'exécutent avec
`node --test web/client.test.mjs`.

Validation locale sur cette révision : API complète **124 passed, 4 xfailed**, couverture
API **98,06 %**, Ruff et mypy sans remarque, tests Node du client web **12 passed**. Les quatre `xfail` sont les erreurs
du modèle déjà documentées dans le jeu d'or. La CI est configurée pour rejouer ces contrôles;
elle ne peut être observée sur GitHub qu'après configuration du dépôt distant et push.
