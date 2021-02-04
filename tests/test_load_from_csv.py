import unittest
from app.run_server import App
from api.load_from_csv import LoadFromCsv
from tests.api_response import ApiReponse
from api.jwt import JWT

class TestTheProjectMethods(unittest.TestCase):
    def setUp(self):
        self.app = App.create_app_instance([LoadFromCsv]).test_client()

    def test_get_methods(self):
        response = ApiReponse(
            self.app.post('/load_from_csv/',
                          # headers={
                          #     'Authorization': 'Bearer ' + JWT.create_access_token(user_name="123", password="456")},
                          data={
                              "server_name": "localhost\sqlexpress",
                              "database_name": "master",
                              "schema_name": "dbo",
                              "table_name": "ms_sql_server_proxy_test",
                              "csv_root_directory": r"c:\temp\ms_sql_server_proxy"
                          },
                          follow_redirects=True))
        self.assertEqual(201, response.status_code)


if __name__ == '__main__':
    unittest.main()
