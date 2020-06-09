from .db_session import SqlAlchemyBase, orm
import sqlalchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    middle_name = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    role_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("roles.id"), nullable=False, default=3)
    role = orm.relation('Roles', backref='users')
    group_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("groups.id"), nullable=True)
    group = orm.relation('Groups', backref='users')


    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __str__(self):
        return self.login

    def __repr__(self):
        return f'<User {self.id} "{self.login}">'

    @property
    def fio(self):
        name = self.name if self.name else ''
        surname = self.surname if self.surname else ''
        middle_name = self.middle_name if self.middle_name else ''
        return f'{name} {surname} {middle_name}'.replace('  ', ' ').strip()

    @property
    def created_date_format(self):
        return self.created_date.strftime("%d.%m.%Y")
