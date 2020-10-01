from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
	APP_DISPLAY_NAME = "Pocket Forum",
	SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/pocket-forum.db' % app.instance_path,
	SQLALCHEMY_TRACK_MODIFICATIONS = False,
	FLASK_ADMIN_SWATCH = 'cerulean',
	)
app.config.from_pyfile('config.py')

from .models import db
from . import jinja2_addons
from . import views
from . import admin
from . import blueprints

db.create_all()

