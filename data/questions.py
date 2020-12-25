from .db_session import SqlAlchemyBase, orm
import sqlalchemy
from get_prepare_text import get_prepare_text


from .distractors import Distractors


class Questions(SqlAlchemyBase):
    __tablename__ = 'questions'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    inner_id = sqlalchemy.Column(sqlalchemy.Integer)
    text = sqlalchemy.Column(sqlalchemy.UnicodeText)
    indexed_text = sqlalchemy.Column(sqlalchemy.UnicodeText)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("subjects.id"), nullable=False)
    subject = orm.relation('Subjects', backref='questions')
    type_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("type_question.id"), nullable=False, default=1)
    type = orm.relation('TypeQuestion', backref='questions')
    ordered = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    completed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)

    text_index = sqlalchemy.Index('text_index', indexed_text)

    def __init__(self, text, subject_id, type_id=1, ordered=False, completed=False, inner_id=None):
        self.text = text.strip()
        self.indexed_text = get_prepare_text(text)
        self.subject_id = subject_id
        self.type_id = type_id
        self.ordered = ordered
        self.completed = completed
        self.inner_id = inner_id


    @property
    def answers(self):
        return [x for x in self.distractors if x.question == self and x.correct]

    @property
    def name(self):
        max_len = 50
        if len(self.text) <= max_len:
            return self.text
        text = self.text[:max_len]
        if ' ' in text:
            text = text[:text.rindex(' ')]
        return text + ' ...'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Questions {self.id} "{self.name}">'

