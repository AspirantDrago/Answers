from .db_session import SqlAlchemyBase
import sqlalchemy


class TypeQuestion(SqlAlchemyBase):
    __tablename__ = 'type_question'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<TypeQuestion {self.id} "{self.title}">'
