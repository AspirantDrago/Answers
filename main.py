from flask import Flask, render_template, request
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


@app.route('/univer/<int:universitet_id>/inst/<int:institute_id>/dep/<int:departament_id>/sub/<int:subject_id>')
def full_subjectLlist(universitet_id, institute_id, departament_id, subject_id):
    universitet = session.query(Universitets).get(universitet_id)
    institute = session.query(Institutes).filter(Institutes.universitet == universitet,
                                                 Institutes.inner_id == institute_id).one()
    departament = session.query(Departments).filter(Departments.institute == institute,
                                                 Departments.inner_id == departament_id).one()
    subj = session.query(Subjects).filter(Subjects.departments == departament,
                                                 Subjects.inner_id == subject_id).one()
    quests = session.query(Questions).filter(Questions.subject == subj).all()
    return render_template('list.html', quests=quests, subj=subj)


@app.route('/univer/<int:universitet_id>/inst/<int:institute_id>/dep/<int:departament_id>/sub/<int:subject_id>/<int:id>')
def question(universitet_id, institute_id, departament_id, subject_id, id):
    universitet = session.query(Universitets).get(universitet_id)
    institute = session.query(Institutes).filter(Institutes.universitet == universitet,
                                                 Institutes.inner_id == institute_id).one()
    departament = session.query(Departments).filter(Departments.institute == institute,
                                                 Departments.inner_id == departament_id).one()
    subj = session.query(Subjects).filter(Subjects.departments == departament,
                                                 Subjects.inner_id == subject_id).one()
    quest = session.query(Questions).filter(Questions.subject == subj, Questions.inner_id == id).one()
    return render_template('quest.html', quest=quest)


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        try:
            text = request.form.get('text', '')
            inner_id = int(request.form.get('inner_id', 0))
            answer = request.form.get('answer', '')
            if text and answer:
                subj = session.query(Subjects).get(1)
                q = Questions(
                    inner_id=inner_id,
                    text=text,
                    subject=subj,
                    completed=True
                )
                session.add(q)
                session.commit()
                a = Distractors(
                    text=answer,
                    question=q,
                    correct=True
                )
                session.add(a)
                session.commit()
        except BaseException:
            pass
    return render_template('new.html')


if __name__ == '__main__':
    port_run = int(os.environ.get("PORT", PORT))
    app.run(host=HOST, port=port_run, debug=DEBUG)
