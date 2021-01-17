import unittest
from api.app import App
from api.upsert import UpsertByRecord
from tests.api_response import ApiReponse
from api.jwt import JWT
import pandas as pd
from zeppos_microsoft_sql_server.ms_sql_server import MsSqlServer
import pyodbc

class TestTheProjectMethods(unittest.TestCase):
    def setUp(self):
        self.app = App.create_app_instance([UpsertByRecord]).test_client()

    def test_1_get_methods(self):
        ms_sql = MsSqlServer("DRIVER={ODBC Driver 13 for SQL Server}; SERVER=localhost\sqlexpress; DATABASE=master; Trusted_Connection=yes;")
        ms_sql.drop_table("dbo", "api_test_table")
        response = ApiReponse(
            self.app.post('/upsert/by_record',
                          headers={
                              'Authorization': 'Bearer ' + JWT.create_access_token(user_name="123", password="456")},
                          data={
                              "connection_string": "DRIVER={ODBC Driver 13 for SQL Server}; SERVER=localhost\sqlexpress; DATABASE=master; Trusted_Connection=yes;",
                              "dataframe": pd.DataFrame({'column_1': [3600]}, columns=['column_1']).to_json(orient='table'),
                              "table_schema": "dbo",
                              "table_name": "api_test_table",
                              "batch_size": "500",
                          },
                          follow_redirects=True))

        self.assertEqual(201, response.status_code)
        self.assertEqual(1, pd.read_sql("SELECT TOP 1 column_1 FROM dbo.api_test_table", pyodbc.connect(
            "DRIVER={ODBC Driver 13 for SQL Server}; SERVER=localhost\sqlexpress; DATABASE=master; Trusted_Connection=yes;")).shape[
            0])

    def test_2_get_methods(self):
        ms_sql = MsSqlServer(
            "DRIVER={ODBC Driver 13 for SQL Server}; SERVER=localhost\sqlexpress; DATABASE=master; Trusted_Connection=yes;")
        ms_sql.drop_table("dbo", "api_test_table")
        ms_sql.create_table("dbo", "api_test_table", pd.DataFrame({'column_1': [3600]}, columns=['column_1']))
        response = ApiReponse(
            self.app.post('/upsert/by_record',
                          headers={
                              'Authorization': 'Bearer ' + JWT.create_access_token(user_name="123", password="456")},
                          data={
                              "connection_string": "DRIVER={ODBC Driver 13 for SQL Server}; SERVER=localhost\sqlexpress; DATABASE=master; Trusted_Connection=yes;",
                              "dataframe": pd.DataFrame({'column_1': [3600]}, columns=['column_1']).to_json(orient='table'),
                              "table_schema": "dbo",
                              "table_name": "api_test_table",
                              "batch_size": "500",
                          },
                          follow_redirects=True))

        self.assertEqual(201, response.status_code)
        self.assertEqual(1, pd.read_sql("SELECT TOP 1 column_1 FROM dbo.api_test_table", pyodbc.connect(
            "DRIVER={ODBC Driver 13 for SQL Server}; SERVER=localhost\sqlexpress; DATABASE=master; Trusted_Connection=yes;")).shape[
            0])


if __name__ == '__main__':
    unittest.main()
