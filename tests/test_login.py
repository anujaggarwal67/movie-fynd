import json

from tests.BaseCase import BaseCase


# test case for checking api for User login
class TestUserLogin(BaseCase):

    def test_successful_login(self):
        # Given
        email = "paurakh011@gmail.com"
        password = "mycoolpassword"
        payload = json.dumps({
            "email": email,
            "password": password
        })
        response = self.app.post('/api/signup', headers={"Content-Type": "application/json"}, data=payload)

        # When
        response = self.app.post('/api/login', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        
        self.assertEqual(200, response.status_code)
        