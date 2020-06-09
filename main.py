from flask import Flask
import os
import logging
from flask_login import LoginManager, logout_user, login_required
from flask_admin import Admin
from flask_babelex import Babel


from config import *
from data.users import User
from data.roles import Roles
from data.universitets import Universitets
from data.institutes import Institutes
from data.departments import Departments
from data.groups import Groups
from data.type_question import TypeQuestion
from data.subjects import Subjects
from data.questions import Questions
from data.distractors import Distractors
from admin_view import *


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
logging.basicConfig(level=logging.INFO)
app.config['FLASK_ADMIN_SWATCH'] = FLASK_ADMIN_SWATCH
admin = Admin(app, template_mode='bootstrap3', name='Административная панель')
admin.add_view(UserAdminModelView(User, session, name='Пользователи'))
admin.add_view(RoleAdminModelView(Roles, session, name='Роли'))
admin.add_view(AdminModelView(Universitets, session, name='Университеты'))
admin.add_view(AdminModelView(Institutes, session, name='Институты'))
admin.add_view(AdminModelView(Departments, session, name='Кафедры'))
admin.add_view(AdminModelView(Groups, session, name='Группы'))
admin.add_view(AdminModelView(TypeQuestion, session, name='Типы вопросов'))
admin.add_view(AdminModelView(Subjects, session, name='Дисциплины'))
admin.add_view(AdminModelView(Questions, session, name='Вопросы'))
admin.add_view(AdminModelView(Distractors, session, name='Варианты ответов'))
babel = Babel(app)


@babel.localeselector
def get_locale():
        return 'ru'


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


if __name__ == '__main__':
    port_run = int(os.environ.get("PORT", PORT))
    app.run(host=HOST, port=port_run, debug=DEBUG)
