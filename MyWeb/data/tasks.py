import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Tasks(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    topic_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("topics.id"))
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    ans = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    lang = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

    # полноценный объект класса Topics
    topic = orm.relation('Topics')

