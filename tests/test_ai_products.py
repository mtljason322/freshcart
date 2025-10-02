"""
Tests d’intégration pour /products.
"""

from __future__ import annotations

from datetime import date, timedelta

from fastapi.testclient import TestClient

from freshcart.api.main import create_app


def test_create_and_list_regular_product() -> None:
    app = create_app()
    client = TestClient(app)

    payload = {"sku": "P1", "name": "Café", "initial_price": 8.0, "type": "regular"}
    r = client.post("/products", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["sku"] == "P1"
    assert data["type"] == "regular"
    assert data["final_price"] == 8.0

    r2 = client.get("/products")
    assert r2.status_code == 200
    items = r2.json()
    assert any(it["sku"] == "P1" for it in items)


def test_perishable_requires_expiry_date() -> None:
    app = create_app()
    client = TestClient(app)

    bad = {"sku": "X1", "name": "Lait", "initial_price": 4.0, "type": "perishable"}
    r = client.post("/products", json=bad)
    assert r.status_code == 422  # pydantic valide: expiry_date requis


def test_perishable_discount_rule() -> None:
    app = create_app()
    client = TestClient(app)

    soon = date.today() + timedelta(days=2)  # <= 3 jours -> -50%
    payload = {
        "sku": "X2",
        "name": "Yaourt",
        "initial_price": 3.0,
        "type": "perishable",
        "expiry_date": soon.isoformat(),
    }
    r = client.post("/products", json=payload)
    assert r.status_code == 201
    assert r.json()["final_price"] == 1.5


def test_duplicate_sku_rejected() -> None:
    app = create_app()
    client = TestClient(app)

    p = {"sku": "DUP", "name": "Sucre", "initial_price": 2.0}
    assert client.post("/products", json=p).status_code == 201
    r = client.post("/products", json=p)
    assert r.status_code == 400
    assert r.json()["detail"] == "SKU already exists"
