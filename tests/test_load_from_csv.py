import unittest
from app.run_server import App
from api.load_from_csv import LoadFromCsv
from tests.api_response import ApiReponse
from zeppos_logging.app_logger import AppLogger
from tests.util_for_testing import UtilForTesting
from zeppos_microsoft_sql_server.ms_sql_server import MsSqlServer
from api.jwt import JWT
import os


class TestTheProjectMethods(unittest.TestCase):
    def setUp(self):
        UtilForTesting.file_clean_up()
        self.app = App.create_app_instance([LoadFromCsv]).test_client()

    def tearDown(self):
        UtilForTesting.file_clean_up()

    def test_get_methods(self):
        AppLogger.configure_and_get_logger("test_logger")
        AppLogger.set_debug_level()

        temp_dir, file_dir, full_file_name_list = UtilForTesting.file_setup('test_df_3', extension="",
                                                                            content="col1|col2\ntest1|test2\ntest1|test2\ntest1|test2\ntest1|test2\ntest1|test2",
                                                                            count=2)

        response = ApiReponse(
            self.app.post('/load_from_csv/',
                          # headers={
                          #     'Authorization': 'Bearer ' + JWT.create_access_token(user_name="123", password="456")},
                          data={
                              "server_name": "localhost\sqlexpress",
                              "database_name": "master",
                              "schema_name": "dbo",
                              "table_name": "ms_sql_server_proxy_load_from_csv_1",
                              "csv_root_directory": file_dir
                          },
                          follow_redirects=True))
        self.assertEqual(201, response.status_code)
        for file in full_file_name_list:
            self.assertEqual(True, os.path.exists(f"{file}.done"))

        ms_sql = MsSqlServer(
            "DRIVER={ODBC Driver 13 for SQL Server}; SERVER=localhost\sqlexpress; DATABASE=master; Trusted_Connection=yes;")
        df = ms_sql.read_data_into_dataframe("select count(1) as record_count from [dbo].[ms_sql_server_proxy_load_from_csv_1]")
        self.assertEqual(10, df.iloc[0]['record_count'])


if __name__ == '__main__':
    unittest.main()
