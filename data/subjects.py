from .db_session import SqlAlchemyBase, orm
import sqlalchemy


class Subjects(SqlAlchemyBase):
    __tablename__ = 'subjects'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    inner_id = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    departments_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("departments.id"), nullable=False)
    departments = orm.relation('Departments', backref='subjects')

    def __init__(self, name, departments_id, inner_id=None):
        self.name = name
        self.departments_id = departments_id
        self.inner_id = inner_id

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Subjects {self.id} "{self.name}">'
