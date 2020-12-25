from .db_session import SqlAlchemyBase, orm
import sqlalchemy


class Departments(SqlAlchemyBase):
    __tablename__ = 'departments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    inner_id = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    institut_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("institutes.id"), nullable=False, default=3)
    institute = orm.relation('Institutes', backref='departments')

    def __init__(self, name, institut_id, inner_id=None):
        self.name = name
        self.institut_id = institut_id
        self.inner_id = inner_id

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Departments {self.id} "{self.name}">'
