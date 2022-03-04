import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


# наследуем от объекта класса SqlAlchemyBase
class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    applic = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    teach = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    solutions = orm.relation("Solutions", back_populates='user')

    # вывод пользователя с заданными параметрами
    def __repr__(self):
        return f'<User> {self.id} {self.name} {self.email} {self.admin}'

    #  устанавливает значение хэша пароля для переданной строки
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    # проверяет, правильный ли пароль ввел пользователь
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)