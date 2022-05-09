from flask_restful import reqparse, abort, Resource
from database.db_session import create_session
from database.user import User
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user


def abort_if_not_found(user_id):
    session = create_session()
    with session.begin():
        user = session.query(User).get(user_id)

        if not user:
            return abort(404, message=f"User {user_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('phone', required=True)
parser.add_argument('password', required=True)
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('is_admin', required=True, type=bool)


class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        abort_if_not_found(user_id)

        if int(user_id) != int(current_user.id) and not current_user.is_admin:
            return abort(403, message="Access denied")

        session = create_session()
        with session.begin():
            user = session.query(User).get(user_id)
            return jsonify({'user': user.to_dict(
                only=('phone', 'name', 'surname', 'bookings', 'is_admin'))})

    @jwt_required()
    def put(self, user_id):
        abort_if_not_found(user_id)
        args = parser.parse_args()

        if int(user_id) != int(current_user.id) and not current_user.is_admin:
            return abort(403, message="Access denied")
        if not current_user.is_admin and args['is_admin']:
            return abort(403, message="Action forbidden")
        if current_user.is_admin and not args['is_admin']:
            return abort(403, message="Action forbidden")

        session = create_session()
        with session.begin():
            user = session.query(User).get(user_id)
            user.phone = args['phone']
            user.set_password(args['password'])
            user.name = args['name']
            user.surname = args['surname']
            user.is_admin = args['is_admin']
        
        return jsonify({'success': 'OK'})
    
    @jwt_required()
    def delete(self, user_id):
        abort_if_not_found(user_id)

        if int(user_id) != int(current_user.id) and not current_user.is_admin:
            return abort(403, message="Access denied")

        session = create_session()
        with session.begin():
            user = session.query(User).get(user_id)
            session.delete(user)
        
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    @jwt_required()
    def get(self):
        if not current_user.is_admin:
            return abort(403, message="Access denied")

        session = create_session()
        with session.begin():
            users = session.query(User).all()
            return jsonify({'bookings': [item.to_dict(
                only=('phone', 'surname', 'name', 'bookings')) for item in users]})
            
    def post(self):
        session = create_session()
        args = parser.parse_args()

        if args['is_admin']:
            return abort(403, message='Action forbidden')

        with session.begin():
            user = User(
                phone=args['phone'],
                surname=args['surname'],
                name=args['name'],
                is_admin=False
            )
            user.set_password(args['password'])
            session.add(user)
        
        return jsonify({'success': 'OK'})
