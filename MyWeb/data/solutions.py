import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Solutions(SqlAlchemyBase):
    __tablename__ = 'solutions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_task = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("tasks.id"))
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.String, default='Не указан!')
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("users.id"))

    user = orm.relation('User')