from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
	APP_DISPLAY_NAME = "Pocket Forum",
	SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/pocket-forum.db' % app.instance_path,
	SQLALCHEMY_TRACK_MODIFICATIONS = False,
	FLASK_ADMIN_SWATCH = 'cerulean',
	)
app.config.from_pyfile('config.py')

from .csrf import csrf_protect
csrf_protect(app)

from .login import login_manager
login_manager.init_app(app)

from . import jinja2_functions
from . import admin
from . import views

