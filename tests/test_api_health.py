"""
Test d’intégration de l’endpoint /health.

On utilise TestClient (synchrones) pour aller vite.
Plus tard, on pourra switcher vers httpx.AsyncClient pour des tests async.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from freshcart.api.main import create_app


def test_health_returns_ok() -> None:
    app = create_app()
    client = TestClient(app)

    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
