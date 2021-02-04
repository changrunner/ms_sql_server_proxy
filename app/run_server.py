# Make sure we have the correct relative path
from sys import path, exc_info, stdout
path.insert(0, '..')  # chang to the root directory of the project
#########################################################################
from zeppos_logging.app_logger import AppLogger
from zeppos_logging.app_logger_json_conifg_name import AppLoggerJsonConfigName
from waitress import serve
import socket
from paste.translogger import TransLogger
from flask import Flask
from flask_restful import Api
from api.heart_beat import HeartBeat
from api.execute import Execute
from api.read import Read
from app.run_app_base import RunAppBase
from api.upsert_by_record import UpsertByRecord
from api.extract_to_csv import ExtractToCsv
from api.load_from_csv import LoadFromCsv
from flasgger import Swagger


class RunServer(RunAppBase):
    def __init__(self):
        super().__init__()

    def run_server(self):
        if super().start_app():
            LISTEN = f"127.0.0.1:{5800}"
            serve(TransLogger(application=App.create_app_instance([HeartBeat, Read, Execute, UpsertByRecord,
                                                                   ExtractToCsv, LoadFromCsv]),
                              logger=AppLogger.logger,
                              setup_console_handler=True)
                  , listen=LISTEN)
            # , Read, Upsert, Execute


class App:
    def create_app(self, class_object_list):
        AppLogger.logger.info("creating app")
        flask_app = Flask(__name__)
        # swagger = Swagger(flask_app)
        api = Api(flask_app)
        for class_object in class_object_list:
            class_object.add_routes(api)

        return flask_app

    @staticmethod
    def create_app_instance(class_object_list):
        AppLogger.logger.info("Create App Instance")
        return App().create_app(class_object_list)


if __name__ == '__main__':
    AppLogger.configure_and_get_logger(
        'ms_sql_server_proxy_monitor',
        AppLoggerJsonConfigName.default_with_watchtower_format_1(),
        watchtower_log_group="ms_sql_server_proxy",
        watchtower_stream_name="app"
    )
    AppLogger.set_debug_level()
    RunServer().run_server()

