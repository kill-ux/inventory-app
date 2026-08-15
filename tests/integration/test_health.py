def test_health_endpoint(client, app_url):
    resp = client.get(f"{app_url}/health")

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "services": {"database": "up"}}

def test_delete_movies(client, app_url):
    resp = client.delete(f"{app_url}/api/movies")
    assert resp.status_code == 204
    assert resp.text == ""

def test_create_movie(client, app_url):
    movie_data = {"title": "Test Movie", "description": "A test movie description"}
    resp = client.post(f"{app_url}/api/movies", json=movie_data)
    assert resp.status_code == 201
    assert resp.json()["title"] == movie_data["title"]
    assert resp.json()["description"] == movie_data["description"]

def test_list_movies(client, app_url):
    resp = client.get(f"{app_url}/api/movies")
    movie_data = {
        "description": "A test movie description",
        "title": "Test Movie",
    }
    assert resp.status_code == 200
    res = resp.json()
    assert res[0]["title"] == movie_data["title"]
    assert res[0]["id"] is not None
    assert len(res) == 1
