from flask_restful import Resource
from zeppos_logging.app_logger import AppLogger
from flasgger import swag_from

heartbeat_specs_dict = {
        "responses": {
            "200": {
                "description": "Returns a heartbeat string",
            }
        }
    }

class HeartBeat(Resource):
    @swag_from(heartbeat_specs_dict)
    def get(self):
        AppLogger.logger.debug("Called Heartbeat")
        return {'alive': 'true'}

    @staticmethod
    def add_routes(api):
        api.add_resource(HeartBeat, '/heartbeat/')





