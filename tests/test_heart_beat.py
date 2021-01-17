import unittest
from api.app import App
from api.heart_beat import HeartBeat
from tests.api_response import ApiReponse

class TestTheProjectMethods(unittest.TestCase):
    def setUp(self):
        self.app = App.create_app_instance([HeartBeat]).test_client()

    def test_get_methods(self):
        response = ApiReponse(self.app.get('/heartbeat/', follow_redirects=True))
        self.assertEqual(200, response.status_code)
        self.assertEqual('{"alive":"true"}', response.content)


if __name__ == '__main__':
    unittest.main()
