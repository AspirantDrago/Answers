from .db_session import SqlAlchemyBase, orm
import sqlalchemy


class Questions(SqlAlchemyBase):
    __tablename__ = 'questions'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    inner_id = sqlalchemy.Column(sqlalchemy.Integer)
    text = sqlalchemy.Column(sqlalchemy.UnicodeText)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("subjects.id"), nullable=False)
    subject = orm.relation('Subjects', backref='questions')
    type_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("type_question.id"), nullable=False, default=1)
    type = orm.relation('TypeQuestion', backref='questions')
    ordered = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    completed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)


    @property
    def name(self):
        return str(self.text)[:20]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Questions {self.id} "{self.name}">'
