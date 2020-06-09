from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect


class AdminModelView(ModelView):
    def is_accessible(self):
        # TODO
        return True
        return current_user.is_authenticated and \
               current_user.role.index >= 1000

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/')


class UserAdminModelView(AdminModelView):
    excluded_list_columns = ('hashed_password',)
    form_excluded_columns = ('hashed_password',)
    column_list = ('id', 'login', 'fio', 'role', 'created_date')
    column_labels = dict(
        login='Логин',
        role='Роль',
        hashed_password='MD5-хэш пароля',
        created_date='Дата и время регистрации',
        name='Имя',
        surname='Фамилия',
        middle_name='Отчество',
        fio='ФИО'
    )


class NoUsersAdminModelView(AdminModelView):
    excluded_list_columns = ('users',)
    form_excluded_columns = ('users',)


class RoleAdminModelView(NoUsersAdminModelView):
    column_labels = dict(
        title='Название',
        index='Уровень',
    )
    column_descriptions = dict(
        index='чем выше - тем больше привелегий'
    )
