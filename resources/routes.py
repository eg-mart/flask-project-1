def init_routes(api):
    from resources.bookings_resources import BookingResource, BookingListResource
    from resources.users_resources import UserResource, UserListResource
    from resources.jwt_authorization import LoginResource
    from resources.bookings_resources import OccupiedTimeResource
    
    api.add_resource(BookingListResource, '/api/v1/bookings')
    api.add_resource(BookingResource, '/api/v1/bookings/<booking_id>')
    api.add_resource(UserListResource, '/api/v1/users')
    api.add_resource(UserResource, '/api/v1/users/<user_id>')
    api.add_resource(LoginResource, '/api/v1/login')
    api.add_resource(OccupiedTimeResource, '/api/v1/occupied-time')
