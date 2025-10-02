from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI

from freshcart.domain.inventory import Inventory  # NEW


def create_app(settings: Dict[str, Any] | None = None) -> FastAPI:
    """
    Factory d'application (recommandée):
    - facilite les tests
    - permet d'injecter des settings plus tard
    """
    app = FastAPI(
        title="FreshCart API",
        version="0.1.0",
        description="API d'entraînement pour gérer des produits/inventaires.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    settings = settings or {}

    # --- état applicatif en mémoire (pour le sprint actuel) ---
    app.state.inventory = Inventory()  # NEW

    # --- routers ---
    from .routers import health, products  # NEW

    app.include_router(health.router)
    app.include_router(products.router)  # NEW

    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "freshcart.api.main:create_app",
        factory=True,
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
