import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Topics(SqlAlchemyBase):
    __tablename__ = 'topics'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # получим все задачи по теме
    tasks = orm.relation("Tasks", back_populates='topic')
