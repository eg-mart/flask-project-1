import sqlalchemy
from sqlalchemy.orm import relationship
from database.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Booking(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'bookings'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = Column(sqlalchemy.Integer, 
                     sqlalchemy.ForeignKey('users.id'))
    user = relationship("User", back_populates="bookings")
    tables = sqlalchemy.Column(sqlalchemy.String)
    datetime = sqlalchemy.Column(sqlalchemy.DateTime)
    duration = sqlalchemy.Column(sqlalchemy.Integer)
