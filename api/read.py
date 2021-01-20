from flask_restful import reqparse, Resource
from zeppos_logging.app_logger import AppLogger
from zeppos_microsoft_sql_server.ms_sql_server import MsSqlServer
# from flasgger import swag_from
# from api.jwt_decorator import login_required

class Read(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('connection_string')
    parser.add_argument('sql_statement')

    # @login_required
    # @swag_from(read_specs_dict)
    def post(self):
        try:
            args = Read.parser.parse_args()
            AppLogger.logger.debug("Calling Api Read Method")
            AppLogger.logger.debug(f"connection_string: {args['connection_string']}")
            AppLogger.logger.debug(f"sql_statement: {args['sql_statement']}")
            ms_sqlserver = MsSqlServer(args['connection_string'])
            df = ms_sqlserver.read_data_into_dataframe(args['sql_statement'])
            AppLogger.logger.debug(f"Retrieved {df.shape[0]} records.")
            return df.to_json(orient='table'), 200
        except Exception as error:
            AppLogger.logger.error(f"Calling Api Read Method Error: {error}")
            return None, 500

    @staticmethod
    def add_routes(api):
        api.add_resource(Read, '/read/')


