import sqlalchemy
from sqlalchemy.orm import relationship
from db_session import SqlAlchemyBase


class Booking(SqlAlchemyBase):
    __tablename__ = 'bookings'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = Column(sqlalchemy.Integer, 
                     sqlalchemy.ForeignKey('users.id'))
    user = relationship("User", back_populates="bookings")
