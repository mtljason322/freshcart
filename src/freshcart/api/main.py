"""
Point d’entrée de l’API FreshCart.

FC-4 : on introduit une *app factory* FastAPI : `create_app()`.
- Une "factory" renvoie une instance d'application configurée.
- Avantages :
  - Tests faciles (tu crées une app isolée par test).
  - Config différente selon l'environnement (dev/test/prod).
  - Évite le code global exécuté au moment de l'import.

⚠️ Pas de routes ici : elles arrivent en FC-5 (health, products, inventory...).
"""

from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI


def create_app(settings: Dict[str, Any] | None = None) -> FastAPI:
    """
    Crée et configure l'application FastAPI.

    Args:
        settings: dictionnaire optionnel de configuration (FC-7/8 : on
        pourra y passer des choses comme DATABASE_URL, LOG_LEVEL, etc.)

    Returns:
        Instance FastAPI prête à l'emploi (sans routes pour l’instant).
    """
    # 1) Créer l'instance
    app = FastAPI(
        title="FreshCart API",
        version="0.1.0",
        description="API d'entraînement pour gérer des produits/inventaires.",
        docs_url="/docs",         # Swagger UI
        redoc_url="/redoc",       # Redoc (autre UI)
        openapi_url="/openapi.json",
    )

    # 2) Appliquer une config basique si fournie
    settings = settings or {}
    # Exemple (plus tard) : app.state.db = make_db(settings["DATABASE_URL"])

    # 3) Brancher les routers (FC-5)
    # from .routers import health, products
    # app.include_router(health.router)
    # app.include_router(products.router, prefix="/products", tags=["products"])
    from .routers import health
    app.include_router(health.router)

    # 4) Middlewares (CORS, sécurité) viendront plus tard

    return app


# Exécution locale (dev) avec `python -m freshcart.api.main`
# → C'est pratique quand tu ne veux pas mémoriser la commande uvicorn.
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "freshcart.api.main:create_app",  # module:callable (factory)
        factory=True,                     # indique à uvicorn que c'est une factory
        host="127.0.0.1",
        port=8000,
        reload=True,                      # auto-reload en dev
    )
