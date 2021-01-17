# Make sure we have the correct relative path
from sys import path, exc_info, stdout
path.insert(0, '..')  # chang to the root directory of the project
#########################################################################
from flask import Flask
from flask_restful import Api
from api.heart_beat import HeartBeat
# from api.execute import Execute
# from api.read import Read
# from api.upsert import Upsert
from flasgger import Swagger

class App:
    def create_app(self, class_object_list):
        flask_app = Flask(__name__)
        swagger = Swagger(flask_app)
        api = Api(flask_app)
        for class_object in class_object_list:
            class_object.add_routes(api)

        return flask_app

    @staticmethod
    def create_app_instance(class_object_list):
        return App().create_app(class_object_list)


if __name__ == '__main__':
    App.\
        create_app_instance([HeartBeat]).\
        run(debug=True, port=5800)
#     , Read, Upsert, Execute
