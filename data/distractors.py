from .db_session import SqlAlchemyBase, orm
import sqlalchemy


class Distractors(SqlAlchemyBase):
    __tablename__ = 'distractors'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.UnicodeText)
    question_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("questions.id"), nullable=False)
    question = orm.relation('Questions', backref='distractors')
    position = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=1)
    correct = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)


    @property
    def name(self):
        return str(self.text)[:100]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Distractors {self.id} "{self.name}">'
