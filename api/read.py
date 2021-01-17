from flask_restful import reqparse, Resource
from api.jwt_decorator import login_required
from zeppos_microsoft_sql_server.ms_sql_server import MsSqlServer

class Read(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('connection_string')
    parser.add_argument('sql_statement')

    @login_required
    def post(self):
        args = Read.parser.parse_args()
        ms_sqlserver = MsSqlServer(args['connection_string'])
        df = ms_sqlserver.read_data_into_dataframe(args['sql_statement'])
        return df.to_json(orient='table'), 201

    @staticmethod
    def add_routes(api):
        api.add_resource(Read, '/read/')


