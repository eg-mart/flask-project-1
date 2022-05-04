from flask_restful import reqparse, abort, Resource
from database.db_session import create_session
from database.booking import Booking
from flask import jsonify


def abort_if_not_found(booking_id):
    session = create_session()
    with session.begin():
        booking = session.query(Booking).get(booking_id)

        if not booking:
            return abort(404, message=f"Booking {booking_id} not found")


class BookingsResource(Resource):
    def get(self, booking_id):
        abort_if_not_found(booking_id)
        session = create_session()

        with session.begin():
            booking = session.query(Booking).get(booking_id)
            return jsonify({'booking': booking.to_dict(
                only=('user_id', 'tables', 'datetime', 'duration'))})
    
    def delete(self, booking_id):
        abort_if_not_found(booking_id)
        session = create_session()

        with session.begin():
            booking = session.query(Booking).get(booking_id)
            session.delete(booking)
        return jsonify({'success': 'OK'})
