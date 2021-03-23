import unittest
import json

from app import app
from database.db import db
from tests.BaseCase import BaseCase

# test case for checking api for signup user
class SignupTest(BaseCase):

    def test_successful_signup(self):
        # Given
        payload = json.dumps({
            "email" : "hello@gmail.com",
            "password": "temppassword"
        })

        response = self.app.post('/api/auth/signup', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(200, response.status_code)

    