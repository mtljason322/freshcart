from __future__ import annotations

from datetime import date, timedelta

from fastapi.testclient import TestClient

from freshcart.api.main import create_app


def test_inventory_value_and_expired() -> None:
    app = create_app()
    client = TestClient(app)

    # 1) 2 produits réguliers
    client.post("/products", json={"sku": "A1", "name": "Café", "initial_price": 8.0})
    client.post("/products", json={"sku": "A2", "name": "Sucre", "initial_price": 2.0})

    # 2) 1 périssable périmé (hier) -> final_price=0.0
    expired_date = (date.today() - timedelta(days=1)).isoformat()
    client.post(
        "/products",
        json={
            "sku": "P0",
            "name": "Yaourt",
            "initial_price": 3.0,
            "type": "perishable",
            "expiry_date": expired_date,
        },
    )

    # 3) 1 périssable bientôt périmé (2 jours) -> -50% sur final_price
    soon_date = (date.today() + timedelta(days=2)).isoformat()
    client.post(
        "/products",
        json={
            "sku": "P2",
            "name": "Lait",
            "initial_price": 4.0,
            "type": "perishable",
            "expiry_date": soon_date,
        },
    )

    # total_value = 8.0 + 2.0 + 0.0 + 2.0 = 12.0
    r_val = client.get("/inventory/value")
    assert r_val.status_code == 200
    assert r_val.json() == {"total_value": 12.0}

    # expired → doit contenir P0
    r_exp = client.get("/products/expired")
    assert r_exp.status_code == 200
    skus = [item["sku"] for item in r_exp.json()]
    assert "P0" in skus
