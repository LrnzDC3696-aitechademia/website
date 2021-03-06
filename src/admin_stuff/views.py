from flask import abort
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        abort(404)


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        abort(404)
