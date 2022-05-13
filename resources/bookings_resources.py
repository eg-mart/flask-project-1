from flask_restful import reqparse, abort, Resource
from database.db_session import create_session
from database.booking import Booking
from database.user import User
from flask import jsonify
from datetime import datetime as dt
from datetime import date
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import func


def abort_if_not_found(booking_id):
    session = create_session()
    with session.begin():
        booking = session.query(Booking).get(booking_id)

        if not booking:
            return abort(404, message=f"Booking {booking_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('tables', required=True)
parser.add_argument('datetime', required=True)
parser.add_argument('duration', required=True, type=int)
parser.add_argument('user_phone', required=True)


class BookingResource(Resource):
    @jwt_required()
    def get(self, booking_id):
        abort_if_not_found(booking_id)

        session = create_session()
        with session.begin():
            booking = session.query(Booking).get(booking_id)

            if int(current_user.id) != int(booking.user_id) and not current_user.is_admin:
                return abort(403, message='Access denied')

            return jsonify({'booking': booking.to_dict(
                only=('user_id', 'tables', 'datetime', 'duration'))})

    @jwt_required()
    def put(self, booking_id):
        abort_if_not_found(booking_id)
        args = parser.parse_args()
        session = create_session()

        datetime = dt.strptime(args['datetime'], "%Y-%m-%d %H:%M:%S")

        with session.begin():
            booking = session.query(Booking).get(booking_id)

            if int(current_user.id) != int(booking.user_id) and not current_user.is_admin:
                return abort(403, message='Access denied')

            user = session.query(User).filter(User.phone == args['user_phone']).one().id
            booking.user_id = user
            booking.duration = args['duration']
            booking.tables = args['tables']
            booking.datetime = datetime
        
        return jsonify({'success': 'OK'})
    
    @jwt_required()
    def delete(self, booking_id):
        abort_if_not_found(booking_id)
        session = create_session()

        if int(current_user.id) != int(booking.user_id) and not current_user.is_admin:
            return abort(403, message='Access denied')

        with session.begin():
            booking = session.query(Booking).get(booking_id)
            session.delete(booking)
        return jsonify({'success': 'OK'})


class BookingListResource(Resource):
    @jwt_required()
    def get(self):
        if not current_user.is_admin:
            return abort(403, message='Access denied')

        session = create_session()
        with session.begin():
            bookings = session.query(Booking).all()
            return jsonify({'bookings':[item.to_dict(
                only=('user_id', 'tables', 'datetime', 'duration')) for item in bookings]})
    
    @jwt_required()
    def post(self):
        session = create_session()
        args = parser.parse_args()

        with session.begin():
            user = session.query(User).filter(User.phone == args['user_phone']).one().id

        if int(current_user.id) != user and not current_user.is_admin:
            return abort(403, message='Access denied')

        datetime = dt.strptime(args['datetime'], "%Y-%m-%d %H:%M:%S")

        with session.begin():
            booking = Booking(
                user_id=user,
                duration=args['duration'],
                datetime=datetime,
                tables=args['tables']
            )
            session.add(booking)

        return jsonify({'success': 'OK'})


date_parser = reqparse.RequestParser()
date_parser.add_argument('date', required=True)


class OccupiedTimeResource(Resource):
    def post(self):
        session = create_session()
        args = date_parser.parse_args()
        with session.begin():
            d = dt.strptime(args["date"], "%Y-%m-%d").date()
            bookings = session.query(Booking).filter(func.date(Booking.datetime) == d).all()
            occupied_time = []
            for booking in bookings:
                start = booking.datetime.hour
                end = int(start + booking.duration / 60)
                occupied_time.append([start, end])
        return jsonify({"occupied_time": occupied_time})
