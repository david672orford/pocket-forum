from flask_admin import Admin
from flask_admin.contrib.sqla.view import ModelView as InsecureModelView
from flask_admin.form import SecureForm
from .models import db
from . import app

# Create base model view
class ModelView(InsecureModelView):
    form_base_class = SecureForm
    action_disallowed_list = ['delete']     # no mass delete

admin = Admin(app, name=app.config['APP_DISPLAY_NAME'])
