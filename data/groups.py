from .db_session import SqlAlchemyBase, orm
import sqlalchemy


class Groups(SqlAlchemyBase):
    __tablename__ = 'groups'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    inner_id = sqlalchemy.Column(sqlalchemy.Integer)
    course = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    institut_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("institutes.id"), nullable=False, default=3)
    institut = orm.relation('Institutes', backref='groups')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Groups {self.id} "{self.name}">'
