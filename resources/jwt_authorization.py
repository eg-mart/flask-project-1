from flask_restful import reqparse, abort, Resource
from database.db_session import create_session
from database.user import User
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required
from resources.jwt_init import jwt


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    session = create_session()

    with session.begin():
        user = session.query(User).get(identity)
        session.expunge(user)
        return user


parser = reqparse.RequestParser()
parser.add_argument('phone', required=True)
parser.add_argument('password', required=True)


class LoginResource(Resource):
    def post(self):
        session = create_session()
        args = parser.parse_args()
        with session.begin():
            user = session.query(User).filter(User.phone == args['phone']).one_or_none()

            if not user or not user.check_password(args['password']):
                return abort(401, message="Wrong username or password")
            
            access_token = create_access_token(identity=user)
            return jsonify(access_token=access_token)
