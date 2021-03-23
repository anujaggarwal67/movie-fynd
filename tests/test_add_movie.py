import json

from tests.BaseCase import BaseCase


# test case for checking api for adding movie
class TestAddingMovie(BaseCase):

    def test_successful_adding_movie(self):
        movie_payload = {
            "name": "Star Wars: The Rise of Skywalker",
            "casts": ["Daisy Ridley", "Adam Driver"],
            "genres": ["Fantasy", "Sci-fi"]
        }
        # When
        response = self.app.post('/api/movies',
            headers={"Content-Type": "application/json"}, data=json.dumps(movie_payload))

        # Then
        self.assertEqual(200, response.status_code)