import unittest
from app.run_server import App
from api.read import Read
from tests.api_response import ApiReponse
import pandas as pd
from io import BytesIO
import json
# from api.jwt import JWT

class TestTheProjectMethods(unittest.TestCase):
    def setUp(self):
        self.app = App.create_app_instance([Read]).test_client()

    def test_get_methods(self):
        response = ApiReponse(
            self.app.post('/read/',
                          # headers={
                          #     'Authorization': 'Bearer ' + JWT.create_access_token(user_name="123", password="456")},
                          data={
                              "connection_string": "DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost\sqlexpress; DATABASE=master; Trusted_Connection=yes;App=Test;",
                              "sql_statement": "select SUSER_NAME() as User_Name, APP_NAME() as app_name"},
                          follow_redirects=True))
        # self.assertEqual(201, response.status_code)
        # df_actual = pd.read_json(BytesIO(json.loads(response.content).encode('utf-8')), orient='table')
        # self.assertEqual(df_actual.iloc[0]["app_name"], 'Test')


if __name__ == '__main__':
    unittest.main()
