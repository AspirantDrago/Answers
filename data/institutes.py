from .db_session import SqlAlchemyBase, orm
import sqlalchemy


class Institutes(SqlAlchemyBase):
    __tablename__ = 'institutes'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    inner_id = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    universitet_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("universitets.id"), nullable=False, default=3)
    universitet = orm.relation('Universitets', backref='institutes')

    def __init__(self, name, universitet_id, inner_id=None):
        self.name = name
        self.universitet_id = universitet_id
        self.inner_id = inner_id

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Institutes {self.id} "{self.name}">'
