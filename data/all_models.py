import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Todo(SqlAlchemyBase):
    __tablename__ = 'todo'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    text = sqlalchemy.Column(sqlalchemy.String(200), nullable=True)
    type = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
