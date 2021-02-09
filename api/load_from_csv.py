from flask_restful import reqparse, Resource
from zeppos_logging.app_logger import AppLogger
# from zeppos_microsoft_sql_server.ms_sql_server import MsSqlServer
# from api.jwt_decorator import login_required
from zeppos_csv.csv_files import CsvFiles
from zeppos_bcpy.sql_configuration import SqlConfiguration


class LoadFromCsv(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('server_name')
    parser.add_argument('database_name')
    parser.add_argument('schema_name')
    parser.add_argument('table_name')
    parser.add_argument('csv_root_directory')
    parser.add_argument('sep')

    # @login_required
    def post(self):
        try:
            args = LoadFromCsv.parser.parse_args()
            AppLogger.logger.debug("Calling Api Execute Method")
            AppLogger.logger.debug(f"server_name: {args['server_name']}")
            AppLogger.logger.debug(f"database_name: {args['database_name']}")
            AppLogger.logger.debug(f"schema_name: {args['schema_name']}")
            AppLogger.logger.debug(f"table_name: {args['table_name']}")
            AppLogger.logger.debug(f"csv_root_directory: {args['csv_root_directory']}")
            AppLogger.logger.debug(f"sep: {args['sep']}")

            clean_sep = args['sep'] if args['sep'] else "|"
            AppLogger.logger.debug(f"clean_sep: {clean_sep}")

            # TODO: coming from unix the csv_root_directory could have the wrong slash for windows.
            CsvFiles(str(args['csv_root_directory']).replace('/', '\\')).to_sql_server_with_chunking(
                sql_configuration=SqlConfiguration(
                    server_type="microsoft",
                    server_name=args['server_name'],
                    database_name=args['database_name'],
                    schema_name=args['schema_name'],
                    table_name=args['table_name']
                ),
                mark_as_processed=True,
                sep=clean_sep
            )

            AppLogger.logger.debug(f"Command Executed")
            return None, 201
        except Exception as error:
            AppLogger.logger.error(f"Calling Api Execute Method Error: {error}")
            return None, 500

    @staticmethod
    def add_routes(api):
        api.add_resource(LoadFromCsv, '/load_from_csv/')
