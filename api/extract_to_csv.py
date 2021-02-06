from flask_restful import reqparse, Resource
from zeppos_logging.app_logger import AppLogger
from zeppos_microsoft_sql_server.ms_sql_server import MsSqlServer
# from api.jwt_decorator import login_required

class ExtractToCsv(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('connection_string')
    parser.add_argument('sql_statement')
    parser.add_argument('csv_root_directory')
    parser.add_argument('csv_file_name')

    # @login_required
    def post(self):
        try:
            args = ExtractToCsv.parser.parse_args()
            AppLogger.logger.debug("Calling Api Execute Method")
            AppLogger.logger.debug(f"connection_string: {args['connection_string']}")
            AppLogger.logger.debug(f"sql_statement: {args['sql_statement']}")
            AppLogger.logger.debug(f"csv_root_directory: {args['csv_root_directory']}")
            AppLogger.logger.debug(f"csv_file_name: {args['csv_file_name']}")


            # TODO: coming from unix the csv_root_directory could have the wrong slash for windows.
            ms_sqlserver = MsSqlServer(args['connection_string'])
            ms_sqlserver.extract_to_csv(
                sql_statement=args['sql_statement'],
                csv_root_directory=str(args['csv_root_directory']).replace('/', '\\'),
                csv_file_name=args['csv_file_name'],
            )

            AppLogger.logger.debug(f"Command Executed")
            return None, 201
        except Exception as error:
            AppLogger.logger.error(f"Calling Api Execute Method Error: {error}")
            return None, 500

    @staticmethod
    def add_routes(api):
        api.add_resource(ExtractToCsv, '/extract_to_csv/')
