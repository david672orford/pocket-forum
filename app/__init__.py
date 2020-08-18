from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
	APP_DISPLAY_NAME = "Pocket Forums",
	SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/pocket-forums.db' % app.instance_path,
	SQLALCHEMY_TRACK_MODIFICATIONS = False,
	FLASK_ADMIN_SWATCH = 'cerulean',
	)
app.config.from_pyfile('config.py')

def format_datetime(the_datetime):
	return "%d-%02d-%02d %02d:%02d" % (the_datetime.year, the_datetime.month, the_datetime.day, the_datetime.hour, the_datetime.minute)
app.jinja_env.filters['datetime'] = format_datetime

from .login import current_user
app.jinja_env.globals['current_user'] = current_user

from . import markdown
from . import admin
from . import views

