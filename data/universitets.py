from .db_session import SqlAlchemyBase
import sqlalchemy


class Universitets(SqlAlchemyBase):
    __tablename__ = 'universitets'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Universitets {self.id} "{self.name}">'
