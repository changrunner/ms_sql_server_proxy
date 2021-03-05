import unittest
from app.run_server import App
from api.extract_to_csv import ExtractToCsv
from tests.api_response import ApiReponse
from api.jwt import JWT

class TestTheProjectMethods(unittest.TestCase):
    def setUp(self):
        self.app = App.create_app_instance([ExtractToCsv]).test_client()

    def test_get_methods(self):
        response = ApiReponse(
            self.app.post('/extract_to_csv/',
                          # headers={
                          #     'Authorization': 'Bearer ' + JWT.create_access_token(user_name="123", password="456")},
                          data={
                              "connection_string": "DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost\sqlexpress; DATABASE=master; Trusted_Connection=yes;",
                              "sql_statement": "select * from information_schema.columns",
                              "csv_root_directory": r"c:\temp\ms_sql_server_proxy",
                              "csv_file_name": "test_file.csv"
                          },
                          follow_redirects=True))
        self.assertEqual(201, response.status_code)

    def test_get_special_unicode_characters_methods(self):
        response = ApiReponse(
            self.app.post('/extract_to_csv/',
                          # headers={
                          #     'Authorization': 'Bearer ' + JWT.create_access_token(user_name="123", password="456")},
                          data={
                              "connection_string": "DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost\sqlexpress; DATABASE=master; Trusted_Connection=yes;",
                              "sql_statement": "select * from dbo.special",
                              "csv_root_directory": r"c:\temp\ms_sql_server_proxy",
                              "csv_file_name": "special.csv"
                          },
                          follow_redirects=True))
        self.assertEqual(201, response.status_code)


if __name__ == '__main__':
    unittest.main()
