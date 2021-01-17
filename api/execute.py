from flask_restful import reqparse, Resource
from api.jwt_decorator import login_required
from zeppos_microsoft_sql_server.ms_sql_server import MsSqlServer

class Execute(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('connection_string')
    parser.add_argument('execute_statement')

    @login_required
    def post(self):
        args = Execute.parser.parse_args()
        ms_sqlserver = MsSqlServer(args['connection_string'])
        ms_sqlserver.execute_sql(args['execute_statement'])
        return None, 201

    @staticmethod
    def add_routes(api):
        api.add_resource(Execute, '/execute/')
