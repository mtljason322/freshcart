"""
Router /health

But pédagogique :
- Avoir une route très simple pour vérifier que l'API est up.
- Servira aussi dans les probes (readiness/liveness) en déploiement.

Points FastAPI utilisés :
- APIRouter pour organiser les endpoints par module.
- Décorateur @router.get pour définir une route HTTP GET.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])  # tag visible dans la doc Swagger


@router.get("/health")
def health() -> dict[str, str]:
    """
    Renvoie un petit JSON "status: ok".

    Retourne:
        dict: {"status": "ok"}
    """
    return {"status": "ok"}
