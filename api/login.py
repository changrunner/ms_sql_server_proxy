from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify, make_response
from api.jwt import JWT
from zeppos_application.app_config import AppConfig

class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email_address')
    parser.add_argument('password')

    def post(self):
        args = Login.parser.parse_args()
        email_address = args['email_address']
        password = args['password']

        if not email_address:
            return make_response(jsonify({"msg": "Missing username parameter"}), 400)
        if not password:
            return make_response(jsonify({"msg": "Missing password parameter"}), 400)

        email_addresses = \
            AppConfig.get_json_config_dict(
                current_module_filename=__file__,
                config_file_name="jwt_config.json"
            )
        if email_addresses is None:
            return make_response(jsonify({"msg": "jwt configuration not completed on the server"}), 500)

        if "email_addresses" in email_addresses and \
                email_address in email_addresses["email_addresses"] and \
                email_addresses["email_addresses"][email_address]:
            return make_response(
                jsonify(
                    access_token=JWT.create_access_token(email_address, password)
                ), 200)

        return make_response(jsonify({"msg": "Bad username or password"}), 401)

    @staticmethod
    def add_routes(api):
        api.add_resource(Login, '/login/')


