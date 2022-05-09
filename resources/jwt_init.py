from flask_jwt_extended import JWTManager


jwt = None


def init_jwt(app):
    global jwt
    jwt = JWTManager(app)
