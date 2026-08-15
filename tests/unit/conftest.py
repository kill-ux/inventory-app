from flask_sqlalchemy.model import _QueryProperty
import pytest
from pytest_mock import MockerFixture
from app import create_app

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

@pytest.fixture
def movie_data():
    """
    {
        "id": 1,
        "title": "Test Movie",
        "description": "A test movie.",
    }
    """
    return {
        "id": 1,
        "title": "Test Movie",
        "description": "A test movie.",
    }



@pytest.fixture
def mock_query(mocker):
    return mocker.Mock()



@pytest.fixture
def mock_add(mocker):
    return mocker.patch(
        "app.routes.movies.db.session.add"
    )

@pytest.fixture
def mock_commit(mocker):
    return mocker.patch(
        "app.routes.movies.db.session.commit"
    )


@pytest.fixture
def mock_session_delete(mocker):
    return mocker.patch(
        "app.routes.movies.db.session.delete"
    )