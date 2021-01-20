from flask_restful import reqparse, Resource
from zeppos_logging.app_logger import AppLogger
from zeppos_microsoft_sql_server.ms_sql_server import MsSqlServer
# from api.jwt_decorator import login_required

class Execute(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('connection_string')
    parser.add_argument('execute_statement')

    # @login_required
    def post(self):
        try:
            args = Execute.parser.parse_args()
            AppLogger.logger.debug("Calling Api Execute Method")
            AppLogger.logger.debug(f"connection_string: {args['connection_string']}")
            AppLogger.logger.debug(f"execute_statement: {args['execute_statement']}")
            ms_sqlserver = MsSqlServer(args['connection_string'])
            ms_sqlserver.execute_sql(args['execute_statement'])
            AppLogger.logger.debug(f"Command Executed")
            return None, 201
        except Exception as error:
            AppLogger.logger.error(f"Calling Api Execute Method Error: {error}")
            return None, 500

    @staticmethod
    def add_routes(api):
        api.add_resource(Execute, '/execute/')
