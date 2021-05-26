from flask import Flask, render_template, request, abort, jsonify
import os
import logging
from flask_login import LoginManager, logout_user, login_required
from flask_admin import Admin
from flask_babelex import Babel
import json
import hashlib
import uuid
from sqlalchemy.orm.exc import NoResultFound
import base64
from waitress import serve

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
# admin.add_view(UserAdminModelView(User, session, name='Пользователи'))
# admin.add_view(RoleAdminModelView(Roles, session, name='Роли'))
# admin.add_view(AdminModelView(Universitets, session, name='Университеты'))
# admin.add_view(AdminModelView(Institutes, session, name='Институты'))
# admin.add_view(AdminModelView(Departments, session, name='Кафедры'))
# admin.add_view(AdminModelView(Groups, session, name='Группы'))
# admin.add_view(AdminModelView(TypeQuestion, session, name='Типы вопросов'))
# admin.add_view(AdminModelView(Subjects, session, name='Дисциплины'))
# admin.add_view(AdminModelView(Questions, session, name='Вопросы'))
# admin.add_view(AdminModelView(Distractors, session, name='Варианты ответов'))
babel = Babel(app)
images = dict()


def prepare_text(text):
    text = text.replace('\n\r', ' ').replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.strip()
    return text


@babel.localeselector
def get_locale():
    return 'ru'


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    result = session.query(User).get(user_id)
    session.close()
    return result


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/univer/<int:universitet_id>/inst/<int:institute_id>/dep/<int:departament_id>/sub/<int:subject_id>',
           methods=['GET', 'POST'])
def full_subjectLlist(universitet_id, institute_id, departament_id, subject_id):
    session = db_session.create_session()
    try:
        universitet = session.query(Universitets).get(universitet_id)
        institute = session.query(Institutes).filter(Institutes.universitet == universitet,
                                                     Institutes.inner_id == institute_id).one()
        departament = session.query(Departments).filter(Departments.institute == institute,
                                                        Departments.inner_id == departament_id).one()
        subj = session.query(Subjects).filter(Subjects.departments == departament,
                                              Subjects.inner_id == subject_id).one()
    except NoResultFound:
        session.rollback()
        session.close()
        return abort(404)
    search_text = prepare_text(request.args.get('search-text', '')).lower()
    if search_text:
        quests = session.query(Questions).filter(
            Questions.subject == subj,
            Questions.indexed_text.like(f'%{search_text}%')
        ).all()
    else:
        quests = session.query(Questions).filter(Questions.subject == subj).all()
    many_pages = False
    indexed_texts_set = set()
    quests2 = []
    for quest in quests:
        indexed_texts_set.add(quest.indexed_text)
        if len(indexed_texts_set) > MAX_SEARCH_ELEMENTS:
            many_pages = True
            break
        quests2.append(quest)
    result = render_template(
        'list.html',
        quests=quests2,
        subj=subj,
        search_text=search_text,
        many_pages=many_pages
    )
    session.close()
    return result


@app.route('/univer/<int:universitet_id>/inst/<int:institute_id>/dep/<int:departament_id>/sub/<int:subject_id>',
           methods=['DELETE'])
def remove_subject(universitet_id, institute_id, departament_id, subject_id):
    session = db_session.create_session()
    try:
        universitet = session.query(Universitets).get(universitet_id)
        institute = session.query(Institutes).filter(Institutes.universitet == universitet,
                                                     Institutes.inner_id == institute_id).one()
        departament = session.query(Departments).filter(Departments.institute == institute,
                                                        Departments.inner_id == departament_id).one()
        subj = session.query(Subjects).filter(Subjects.departments == departament,
                                              Subjects.inner_id == subject_id).one()
        quests = session.query(Questions).filter(Questions.subject == subj).all()
        for quest in quests:
            session.query(Distractors).filter(Distractors.question == quest).delete()
            session.delete(quest)
        session.delete(subj)
        session.commit()
        session.close()
        return jsonify({'OK': 'OK'})
    except NoResultFound:
        session.rollback()
        session.close()
        return jsonify({'error': 'not found'})


@app.route(
    '/univer/<int:universitet_id>/inst/<int:institute_id>/dep/<int:departament_id>/sub/<int:subject_id>/<int:id>')
def question(universitet_id, institute_id, departament_id, subject_id, id):
    session = db_session.create_session()
    search_text = prepare_text(request.args.get('search-text', '')).lower()
    universitet = session.query(Universitets).get(universitet_id)
    institute = session.query(Institutes).filter(Institutes.universitet == universitet,
                                                 Institutes.inner_id == institute_id).one()
    departament = session.query(Departments).filter(Departments.institute == institute,
                                                    Departments.inner_id == departament_id).one()
    subj = session.query(Subjects).filter(Subjects.departments == departament,
                                          Subjects.inner_id == subject_id).one()
    quest = session.query(Questions).filter(Questions.subject == subj, Questions.inner_id == id).one()
    result = render_template('quest.html', quest=quest, search_text=search_text)
    session.close()
    return result


@app.route(
    '/univer/<int:universitet_id>/inst/<int:institute_id>/dep/<int:departament_id>/sub/<int:subject_id>/<int:id>/open')
def question_open(universitet_id, institute_id, departament_id, subject_id, id):
    session = db_session.create_session()
    search_text = prepare_text(request.args.get('search-text', '')).lower()
    universitet = session.query(Universitets).get(universitet_id)
    institute = session.query(Institutes).filter(Institutes.universitet == universitet,
                                                 Institutes.inner_id == institute_id).one()
    departament = session.query(Departments).filter(Departments.institute == institute,
                                                    Departments.inner_id == departament_id).one()
    subj = session.query(Subjects).filter(Subjects.departments == departament,
                                          Subjects.inner_id == subject_id).one()
    quest = session.query(Questions).filter(Questions.subject == subj, Questions.inner_id == id).one()
    result = render_template('quest_open.html', quest=quest, search_text=search_text)
    session.close()
    return result


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        session = db_session.create_session()
        try:
            text = request.form.get('text', '')
            text = prepare_text(text)
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
            session.rollback()
            pass
        finally:
            session.close()
    return render_template('new.html')


@app.route('/api/add_new_image_png', methods=['POST'])
def add_new_image_png():
    try:
        data = base64.b64decode(request.form.get('data').split(',')[1])
        h =  hashlib.sha256(data).hexdigest()
        if h not in images:
            path = r'static/img/' + str(uuid.uuid1()) + '.png'
            with open(path, 'wb') as f:
                f.write(data)
            images[h] = path
        return jsonify({'status': 'ok', 'path': images[h]})
    except BaseException as e:
        return jsonify({'status': 'error', 'error': str(e)})


@app.route('/api/add_new_question', methods=['POST'])
def api_add_new_question():
    session = db_session.create_session()
    try:
        universitet = request.form['universitet']
        if session.query(Universitets).filter(Universitets.name == universitet).count() == 0:
            session.add(Universitets(universitet))
            session.commit()
        universitet_id = int(session.query(Universitets).filter(
            Universitets.name == universitet
        ).one().id)

        institute = request.form['institute']
        institute_inner = request.form.get('institute_inner', None)
        if institute_inner is not None:
            institute_inner = int(institute_inner)
        if session.query(Institutes).filter(
                Institutes.name == institute,
                Institutes.universitet_id == universitet_id
        ).count() == 0:
            session.add(Institutes(institute, universitet_id, institute_inner))
            session.commit()
        institute_id = int(session.query(Institutes).filter(
            Institutes.name == institute,
            Institutes.universitet_id == universitet_id
        ).one().id)

        department = request.form['department']
        department_inner = request.form.get('department_inner', None)
        if department_inner is not None:
            department_inner = int(department_inner)
        if session.query(Departments).filter(
                Departments.name == department,
                Departments.institut_id == institute_id
        ).count() == 0:
            session.add(Departments(department, institute_id, department_inner))
            session.commit()
        department_id = int(session.query(Departments).filter(
            Departments.name == department,
            Departments.institut_id == institute_id
        ).one().id)

        subject = request.form['subject']
        subject_inner = request.form.get('subject_inner', None)
        if subject_inner is not None:
            subject_inner = int(subject_inner)
        if session.query(Subjects).filter(
                Subjects.name == subject,
                Subjects.departments_id == department_id
        ).count() == 0:
            session.add(Subjects(subject, department_id, subject_inner))
            session.commit()
        subject_id = int(session.query(Subjects).filter(
            Subjects.name == subject,
            Subjects.departments_id == department_id
        ).one().id)

        ordered = bool(int(request.form['ordered']))
        ztype = int(request.form['type'])
        count = int(request.form['count'])
        text = request.form['text']
        text = prepare_text(text)
        inner_id = int(request.form['inner_id'])
        answers = [prepare_text(request.form.get(f'answer_{i}', '')) for i in range(count)]

        quest = Questions(text, subject_id, ztype, ordered, True, inner_id)
        session.add(quest)
        session.commit()
        for i in range(count):
            session.add(Distractors(
                text=answers[i],
                question=quest,
                correct=True
            ))
            session.commit()
        session.close()
    except BaseException as e:
        session.rollback()
        session.close()
        return json.dumps({'error': str(e)}), 400, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    images_path = 'static/img'
    for filename in os.listdir(images_path):
        filename = os.path.join(images_path, filename)
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                h = hashlib.sha256(f.read()).hexdigest()
            images[h] = filename.replace('\\', '/')
    print('Количество изображений:', len(images))
    port_run = int(os.environ.get("PORT", PORT))
    if DEBUG:
        app.run(host=HOST, port=port_run, debug=DEBUG)
    else:
        serve(app, host=HOST, port=port_run)

