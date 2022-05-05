from flask_restful import reqparse, abort, Resource
from database.db_session import create_session
from database.booking import Booking
from flask import jsonify
from datetime import datetime as dt


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
parser.add_argument('user_id', required=True, type=int)


class BookingResource(Resource):
    def get(self, booking_id):
        abort_if_not_found(booking_id)
        session = create_session()

        with session.begin():
            booking = session.query(Booking).get(booking_id)
            return jsonify({'booking': booking.to_dict(
                only=('user_id', 'tables', 'datetime', 'duration'))})

    def put(self, booking_id):
        abort_if_not_found(booking_id)
        args = parser.parse_args()
        session = create_session()

        datetime = dt.strptime(args['datetime'], "%a, %d %b %Y %X GMT")

        with session.begin():
            booking = session.query(Booking).get(booking_id)
            booking.user_id = args['user_id']
            booking.duration = args['duration']
            booking.tables = args['tables']
            booking.datetime = datetime
        
        return jsonify({'success': 'OK'})
    
    def delete(self, booking_id):
        abort_if_not_found(booking_id)
        session = create_session()

        with session.begin():
            booking = session.query(Booking).get(booking_id)
            session.delete(booking)
        return jsonify({'success': 'OK'})


class BookingListResource(Resource):
    def get():
        session = create_session()
        with session.begin():
            bookings = session.query(Booking).all()
            return jsonify({'bookings':[item.to_dict(
                only=('user_id', 'tables', 'datetime', 'duration')) for item in bookings]})
    
    def post():
        session = create_session()
        args = parser.parse_args()

        datetime = dt.strptime(args['datetime'], "%a, %d %b %Y %X GMT")

        with session.begin():
            booking = Booking(
                user_id=args['user_id'],
                duration=args['duration'],
                datetime=datetime,
                tables=args['tables']
            )
            session.add(booking)

        return jsonify({'success': 'OK'})
