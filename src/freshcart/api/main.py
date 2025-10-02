from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI

from freshcart.domain.inventory import Inventory

from .routers import health, inventory, products


def create_app(settings: Dict[str, Any] | None = None) -> FastAPI:
    """
    Factory d'application:
    - crée et retourne une instance FastAPI isolée (utile pour tests)
    - point unique pour injecter des settings plus tard (DB, CORS, etc.)
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

    # État applicatif en mémoire pour ce sprint (remplacé plus tard par une DB)
    app.state.inventory = Inventory()

    # Brancher les routers
    app.include_router(health.router)
    app.include_router(products.router)
    app.include_router(inventory.router)

    return app


if __name__ == "__main__":
    import uvicorn

    # Lance uvicorn avec la factory (option factory=True)
    uvicorn.run(
        "freshcart.api.main:create_app",
        factory=True,
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
