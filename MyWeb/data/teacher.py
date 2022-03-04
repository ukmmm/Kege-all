import sqlalchemy

from data.db_session import SqlAlchemyBase


class Teachers(SqlAlchemyBase):
    __tablename__ = 'teachers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    id_name = sqlalchemy.Column(sqlalchemy.NUMERIC, nullable=True)
