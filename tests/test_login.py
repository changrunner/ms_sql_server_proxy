import unittest
from api.app import App
from api.login import Login
from tests.api_response import ApiReponse
import json

class TestTheProjectMethods(unittest.TestCase):
    def setUp(self):
        self.app = App.create_app_instance([Login]).test_client()

    def test_get_methods(self):
        response = ApiReponse(self.app.post('/login/', data={"email_address": "test@test.com", "password": "my_pass_1234"}, follow_redirects=True))
        self.assertEqual(200, response.status_code)
        self.assertGreater(len(json.loads(response.content)['access_token']), 0)


if __name__ == '__main__':
    unittest.main()
