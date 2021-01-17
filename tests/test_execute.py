import unittest
from api.app import App
from api.execute import Execute
from tests.api_response import ApiReponse
from api.jwt import JWT

class TestTheProjectMethods(unittest.TestCase):
    def setUp(self):
        self.app = App.create_app_instance([Execute]).test_client()

    def test_get_methods(self):
        response = ApiReponse(
            self.app.post('/execute/',
                          headers={
                              'Authorization': 'Bearer ' + JWT.create_access_token(user_name="123", password="456")},
                          data={
                              "connection_string": "DRIVER={ODBC Driver 13 for SQL Server}; SERVER=localhost\sqlexpress; DATABASE=master; Trusted_Connection=yes;",
                              "execute_statement": "execute [sys].[sp_columns] 'spt_monitor'"},
                          follow_redirects=True))
        self.assertEqual(201, response.status_code)


if __name__ == '__main__':
    unittest.main()
