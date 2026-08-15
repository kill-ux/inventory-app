from pytest_mock import MockerFixture
from flask_sqlalchemy.model import _QueryProperty


def test_list_movies(client, mocker: MockerFixture, movie_data):
    """
    GET /api/movies/ should return a list of movies.
    """

    
    # 1. Fake movie object
    mock_movie = mocker.Mock()
    mock_movie.to_dict.return_value = movie_data

    # 2. Mock query object with .all() returning our fake movie
    mock_query = mocker.Mock()
    mock_query.all.return_value = [mock_movie]

    # 3. Patch Movie.query on the route's import target
    mocker.patch.object(
        _QueryProperty,
        "__get__",
        return_value=mock_query
    )

    # 4. Make request & assert
    resp = client.get("/api/movies/")

    assert resp.status_code == 200
    assert resp.get_json() == [movie_data]



def test_list_movies_by_title(client, mocker: MockerFixture, movie_data):
    """
    GET /api/movies/?title=Test should return a list of movies filtered by title.
    """

    # 1. Fake movie object
    mock_movie = mocker.Mock()
    mock_movie.to_dict.return_value = movie_data

    mock_query = mocker.Mock()
    mock_query.filter.return_value = [mock_movie]

    mocker.patch.object(
        _QueryProperty,
        "__get__",
        return_value=mock_query
    )

    resp = client.get("/api/movies/?title=Test")

    assert resp.status_code == 200
    assert resp.get_json() == [movie_data]

def test_create_movie_missing_title_return_400(client):
    """
    POST /api/movies/ with missing title should return 400.
    """

    resp = client.post("/api/movies/", json={"description": "A test movie."})

    assert resp.status_code == 400
    assert resp.get_json() == {"error": "Missing or invalid title"}

def test_create_movie_success(client, mocker: MockerFixture, movie_data):
    """
    POST /api/movies/ with valid data should create a movie and return 201.
    """

    mock_movie = mocker.Mock()
    mock_movie.to_dict.return_value = movie_data

    mocker.patch("app.routes.movies.Movie", return_value=mock_movie)

    mocker.patch("app.routes.movies.db.session.add")
    mocker.patch("app.routes.movies.db.session.commit")

    resp = client.post("/api/movies/", json={"title": "Test Movie", "description": "A test movie."})

    assert resp.status_code == 201
    assert resp.get_json() == movie_data

def test_delete_movies(client, mocker: MockerFixture):
    """
    DELETE /api/movies/ should delete all movies and return 204.
    """

    query = mocker.Mock()
    query.delete.return_value = 0

    mocker.patch.object(
        _QueryProperty,
        "__get__",
        return_value=query
    )
    
    mocker.patch("app.routes.movies.db.session.commit")

    resp = client.delete("/api/movies/")

    assert resp.status_code == 204

def test_get_movie_not_found(client, mocker: MockerFixture):
    """
    GET /api/movies/<id> with non-existent id should return 404.
    """

    query = mocker.Mock()
    query.get.return_value = None


    mocker.patch.object(
        _QueryProperty,
        "__get__",
        return_value=query
    )

    resp = client.get("/api/movies/999")

    assert resp.status_code == 404
    assert resp.get_json() == {"error": "Movie not found"}

def test_get_movie_success(client, mocker: MockerFixture, movie_data):
    """
    GET /api/movies/<id> with existing id should return the movie.
    """

    mock_movie = mocker.Mock()
    mock_movie.to_dict.return_value = movie_data

    query = mocker.Mock()
    query.get.return_value = mock_movie

    mocker.patch.object(
        _QueryProperty,
        "__get__",
        return_value=query
    )

    resp = client.get("/api/movies/1")

    assert resp.status_code == 200
    assert resp.get_json() == movie_data

def test_update_movie_success(client, mocker: MockerFixture, movie_data):
    """
    PUT /api/movies/<id> with valid data should update the movie and return 200.
    """

    mock_movie = mocker.Mock()
    mock_movie.to_dict.return_value = movie_data

    query = mocker.Mock()
    query.get.return_value = mock_movie

    mocker.patch.object(
        _QueryProperty,
        "__get__",
        return_value=query
    )

    mocker.patch("app.routes.movies.db.session.commit")

    resp = client.put("/api/movies/1", json={"title": "Updated Movie", "description": "An updated test movie."})

    assert resp.status_code == 200
    assert resp.get_json() == movie_data

def test_update_movie_missing_title_return_400(client, mocker: MockerFixture):
    """
    PUT /api/movies/<id> with missing title should return 400.
    """

    mock_movie = mocker.Mock()

    query = mocker.Mock()
    query.get.return_value = mock_movie

    mocker.patch.object(
        _QueryProperty,
        "__get__",
        return_value=query
    )

    resp = client.put("/api/movies/1", json={"description": "An updated test movie."})

    assert resp.status_code == 400
    assert resp.get_json() == {"error": "Missing or invalid title"}

def test_delete_movie_success(client, mocker: MockerFixture):
    """
    DELETE /api/movies/<id> with existing id should delete the movie and return 204.
    """

    mock_movie = mocker.Mock()

    query = mocker.Mock()
    query.get.return_value = mock_movie

    mocker.patch.object(
        _QueryProperty,
        "__get__",
        return_value=query
    )


    mocker.patch("app.routes.movies.db.session.delete")
    mocker.patch("app.routes.movies.db.session.commit")

    resp = client.delete("/api/movies/1")

    assert resp.status_code == 204
