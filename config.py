from data import db_session
from data.users import User
from data.roles import Roles
from data.type_question import TypeQuestion


db_session.global_init("db/database.sqlite")
HOST = '0.0.0.0'
PORT = 80
SECRET_KEY = 'scada_system'
REMEMBER_USER = False
FLASK_ADMIN_SWATCH = 'Spacelab'
MAX_SEARCH_ELEMENTS = 10


def create_root():
    session = db_session.create_session()
    root_user = session.query(User).filter(User.login == 'root').first()
    if not root_user:
        root_user = User(
            login='root',
            role_id=1
        )
        root_user.set_password('root')
        session.add(root_user)
        session.commit()
    session.close()

def add_default_record(table, params):
    session = db_session.create_session()
    title = params['title']
    record = session.query(table).filter(table.title == title).first()
    if record:
        return False
    new_record = table(**params)
    session.add(new_record)
    session.commit()
    session.close()
    return True


def create_roles():
    add_default_record(Roles, {
        'title': 'Суперадминистратор',
        'index': 1000
    })
    add_default_record(Roles, {
        'title': 'Администратор',
        'index': 500
    })
    add_default_record(Roles, {
        'title': 'Пользователь',
        'index': 0
    })


def create_types_questions():
    add_default_record(TypeQuestion, {
        'title': 'Единичный выбор',
    })
    add_default_record(TypeQuestion, {
        'title': 'Множественный выбор',
    })
    add_default_record(TypeQuestion, {
        'title': 'Открытое задание',
    })


create_roles()
create_root()
create_types_questions()
