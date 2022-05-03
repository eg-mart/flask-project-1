import sqlalchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from database.db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash, generate_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    bookings = relationship("Booking", back_populates="user")
