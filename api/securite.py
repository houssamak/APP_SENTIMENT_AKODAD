"""Authentification par clé d'API et autorisation par rôle."""

import os
import secrets
from collections.abc import Callable
from typing import Annotated, Literal, cast

from fastapi import Depends, HTTPException, Request, Security
from fastapi.security import APIKeyHeader

Role = Literal["client", "admin"]
ROLES = {"client", "admin"}
LONGUEUR_MIN = 16
EN_TETE = APIKeyHeader(name="X-API-Key", auto_error=False)
NON_AUTHENTIFIE = {"WWW-Authenticate": "ApiKey"}


def charger_cles(brut: str | None = None) -> dict[str, Role]:
    """Parse et valide API_KEYS, sans jamais inclure une clé dans les erreurs."""
    valeur = os.environ.get("API_KEYS", "") if brut is None else brut
    cles: dict[str, Role] = {}
    for entree in (partie.strip() for partie in valeur.split(",")):
        if not entree:
            continue
        cle, separateur, role_texte = entree.rpartition(":")
        if not separateur or role_texte not in ROLES:
            raise ValueError("rôle invalide dans API_KEYS (attendu : client ou admin)")
        if len(cle) < LONGUEUR_MIN:
            raise ValueError(
                f"clé trop courte dans API_KEYS ({len(cle)} caractères, minimum {LONGUEUR_MIN})"
            )
        if cle in cles:
            raise ValueError("clé dupliquée dans API_KEYS")
        cles[cle] = cast(Role, role_texte)  # validé ci-dessus
    if not cles:
        raise ValueError("Aucune clé dans API_KEYS : configurez au moins une clé client ou admin")
    return cles


def identifier(
    cle: Annotated[str | None, Security(EN_TETE)], request: Request
) -> Role:
    """Authentifie la clé reçue et renvoie son rôle."""
    if not cle:
        raise HTTPException(401, "Clé d'API manquante : en-tête X-API-Key", headers=NON_AUTHENTIFIE)
    cles: dict[str, Role] = request.app.state.api_keys
    for connue, role in cles.items():
        if secrets.compare_digest(cle.encode(), connue.encode()):
            return role
    raise HTTPException(401, "Clé d'API invalide", headers=NON_AUTHENTIFIE)


def exiger(*autorises: Role) -> Callable[[Role], Role]:
    """Construit une dépendance qui n'autorise que les rôles indiqués."""

    def verifier(role: Annotated[Role, Depends(identifier)]) -> Role:
        if role not in autorises:
            raise HTTPException(403, f"Accès refusé au rôle « {role} »")
        return role

    return verifier
