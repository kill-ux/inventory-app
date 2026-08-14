from pytest_mock import MockerFixture
from flask_sqlalchemy.model import _QueryProperty


def test_list_movies(client, mocker: MockerFixture):
    """
    GET /api/movies/ should return a list of movies.
    """
    
    # 1. Fake movie object
    mock_movie = mocker.Mock()
    mock_movie.to_dict.return_value = {
        "id": 1,
        "title": "Test Movie",
        "description": "A test movie."
    }

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
    assert resp.get_json() == [{
        "id": 1,
        "title": "Test Movie",
        "description": "A test movie."
    }]
    
# def test_list_movies_by_title(client, mocker: MockerFixture):
#     """
#     GET /api/movies/?title=Test should return a list of movies filtered by title.
#     """
    
#     # 1. Fake movie object
#     mock_movie = mocker.Mock()
#     mock_movie.to_dict.return_value = {
#         "id": 1,
#         "title": "Test Movie",
#         "description": "A test movie."
#     }

#     # 2. Mock query object with .filter_by().all() returning our fake movie
#     mock_query = mocker.Mock()
#     mock_query.filter_by.return_value.all.return_value = [mock_movie]

#     # 3. Patch Movie.query on the route's import target
#     mocker.patch.object(
#         _QueryProperty,
#         "__get__",
#         return_value=mock_query
#     )

#     # 4. Make request & assert
#     resp = client.get("/api/movies/?title=Test")

#     assert resp.status_code == 200
#     assert resp.get_json() == [{
#         "id": 1,
#         "title": "Test Movie",
#         "description": "A test movie."
#     }]