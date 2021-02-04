from flask_restful import reqparse, Resource
from api.jwt_decorator import login_required
from zeppos_microsoft_sql_server.ms_sql_server import MsSqlServer
from io import BytesIO
import pandas as pd
import json

class UpsertByRecord(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('connection_string')
    parser.add_argument('dataframe')
    parser.add_argument('table_schema')
    parser.add_argument('table_name')
    parser.add_argument('batch_size')

    # @login_required
    def post(self):
        try:
            args = UpsertByRecord.parser.parse_args()
            ms_sql = MsSqlServer(args['connection_string'])
            df = pd.read_json(BytesIO(args['dataframe'].encode('utf-8')), orient='table')

            table_schema = args['table_schema']
            table_name = args['table_name']
            batch_size = int(args['batch_size'])

            ms_sql.create_table(table_schema, table_name, df)

            if ms_sql.save_dataframe_by_record(df, table_schema, table_name, batch_size):
                return None, 201
            else:
                return "Could not insert data", 500

        except Exception as error:
            return error, 500

    @staticmethod
    def add_routes(api):
        api.add_resource(UpsertByRecord, '/upsert/by_record/')
