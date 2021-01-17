import unittest
from api.app import App
from api.read import Read
from tests.api_response import ApiReponse
import pandas as pd
from io import BytesIO
import json
from api.jwt import JWT

class TestTheProjectMethods(unittest.TestCase):
    def setUp(self):
        self.app = App.create_app_instance([Read]).test_client()

    def test_get_methods(self):
        response = ApiReponse(
            self.app.post('/read/',
                          headers={
                              'Authorization': 'Bearer ' + JWT.create_access_token(user_name="123", password="456")},
                          data={
                              "connection_string": "DRIVER={ODBC Driver 13 for SQL Server}; SERVER=localhost\sqlexpress; DATABASE=master; Trusted_Connection=yes;",
                              "sql_statement": "select count(1) as record_count from information_schema.tables"},
                          follow_redirects=True))
        self.assertEqual(201, response.status_code)
        df_actual = pd.read_json(BytesIO(json.loads(response.content).encode('utf-8')), orient='table')
        self.assertGreater(df_actual.iloc[0]["record_count"], 0)


if __name__ == '__main__':
    unittest.main()
