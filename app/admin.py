# Create a Flask-Admin instance to which components can attach views

from flask import redirect
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla.view import ModelView as InsecureModelView
from flask_admin.form import SecureForm
from .models import db
from . import app

# Create base model view
class ModelView(InsecureModelView):
	form_base_class = SecureForm
	action_disallowed_list = ['delete']     # no mass delete

class MyAdminIndexView(AdminIndexView):
	@expose()
	def index(self):
		return redirect("forumsections/")

admin = Admin(app, name=app.config['APP_DISPLAY_NAME'], index_view=MyAdminIndexView())
admin.menu().pop(0)
