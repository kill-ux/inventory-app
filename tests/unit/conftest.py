import pytest
from pytest_mock import MockerFixture
from app import create_app

# @pytest.fixture
# def client(monkeypatch, mocker: MockerFixture):
#     # Set environment variables
#     monkeypatch.setenv("INVENTORY_DB_USER", "inventory-db")
#     monkeypatch.setenv("INVENTORY_DB_PASS", "inventory-db")
#     monkeypatch.setenv("INVENTORY_DB_NAME", "inventory-db")
#     monkeypatch.setenv("INVENTORY_DB_HOST", "inventory-db")

#     mocker.patch("app.db.create_all")

#     app = create_app()
#     with app.app_context():
#         yield app.test_client()

@pytest.fixture
def app(monkeypatch, mocker: MockerFixture):
    monkeypatch.setenv("INVENTORY_DB_USER", "inventory-db")
    monkeypatch.setenv("INVENTORY_DB_PASS", "inventory-db")
    monkeypatch.setenv("INVENTORY_DB_NAME", "inventory-db")
    monkeypatch.setenv("INVENTORY_DB_HOST", "inventory-db")

    mocker.patch("app.db.create_all")
    mocker.patch("app.models.db.session.execute")

    
    return create_app()

@pytest.fixture
def client(app):
    with app.app_context():
        yield app.test_client()

@pytest.fixture
def fake_upstream_response(mocker):
    resp = mocker.Mock()
    resp.content = b"{}"
    resp.status_code = 200
    resp.headers = {"Content-Type": "application/json"}
    return resp
