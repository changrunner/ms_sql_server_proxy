import python_jwt as jwt
import jwcrypto.jwk as jwk
from datetime import timedelta
# from api.app import App

"""
Based on: https://flask-jwt-extended.readthedocs.io/en/stable/
"""
class JWT:
    _private_key = None
    JWT_cached_tokens = {}

    @staticmethod
    def create_access_token(user_name, password):
        return \
            JWT._set_access_token(
                access_token=jwt.generate_jwt(
                    claims={'user_name': user_name, 'password': password},
                    priv_key=JWT._get_private_key(),
                    algorithm='PS256',
                    lifetime=timedelta(minutes=5)
                ),
                user_name=user_name)

    @staticmethod
    def _get_private_key():
        if not JWT._private_key:
            JWT._private_key = jwk.JWK.generate(kty='RSA', size=2048)

        return JWT._private_key

    @staticmethod
    def _set_access_token(access_token, user_name):
        JWT.JWT_cached_tokens[user_name] = access_token
        return access_token

    @staticmethod
    def verify_access_token(access_token):
        try:
            access_token = access_token[7:]
            JWT._access_token_in_cache(access_token)
            jwt.verify_jwt(
                jwt=access_token,
                pub_key=JWT._get_private_key(),
                allowed_algs=['PS256']
            )
        except Exception as error:
            return False, error, 401

        # If we get to this point. All good.
        # Check the token exists. Not sure it is for the user but we have to assume. That is how jwt works. I think.
        # Token not expired
        return True, "", 200

    @staticmethod
    def _access_token_in_cache(access_token):
        for k, v in JWT.JWT_cached_tokens.items():
            if access_token == v:
                return True

        raise Exception("Unauthorized: Access Token does not exist.")

