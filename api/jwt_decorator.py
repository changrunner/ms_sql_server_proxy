from functools import wraps
from api.jwt import JWT
from flask import jsonify, make_response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        read = args[0]
        read.parser.add_argument('Authorization', location="headers")
        arguments = read.parser.parse_args()

        if 'Authorization' not in arguments:
            return make_response(jsonify({"msg": "Header not found"}), 401)

        valid_token, msg, statuscode = JWT.verify_access_token(arguments['Authorization'])
        if not valid_token:
            return make_response(jsonify({"msg": "unauthorized"}), 401)

        return f(*args, **kwargs)
    return decorated_function

