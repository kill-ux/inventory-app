import pytest, os, requests

@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL", "http://localhost:8000")

@pytest.fixture(scope="session")
def client(app_url):
    """Provide a requests session for testing."""
    session = requests.Session()
    session.base_url = app_url
    yield session
    session.close()