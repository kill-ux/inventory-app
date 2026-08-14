import pytest
from app import create_app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("INVENTORY_DB_USER", "inventory-db")
    monkeypatch.setenv("INVENTORY_DB_PASS", "inventory-db")
    monkeypatch.setenv("INVENTORY_DB_NAME", "nventory-db")
    monkeypatch.setenv("INVENTORY_DB_HOST", "nventory-db")

    app = create_app()
    return app.test_client()


@pytest.fixture
def fake_upstream_response(mocker):
    resp = mocker.Mock()
    resp.content = b"{}"
    resp.status_code = 200
    resp.headers = {"Content-Type": "application/json"}
    return resp
