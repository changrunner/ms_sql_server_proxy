import unittest
from api.jwt import JWT
from app.run_server import App

class TestTheProjectMethods(unittest.TestCase):
    def test_create_access_token_method(self):
        self.assertGreater(len(JWT.create_access_token(user_name="123", password="456")), 0)
        self.assertGreater(len(JWT.JWT_cached_tokens["123"]), 0)

    def test_verify_access_token_method(self):
        access_token = 'Bearer ' + JWT.create_access_token(user_name="123", password="456")
        self.assertEqual((True, '', 200), JWT.verify_access_token(access_token))


if __name__ == '__main__':
    unittest.main()