from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
	APP_DISPLAY_NAME = "Pocket Forums",
	SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/pocket-forums.db' % app.instance_path,
	SQLALCHEMY_TRACK_MODIFICATIONS = False,
	FLASK_ADMIN_SWATCH = 'cerulean',
	)
app.config.from_pyfile('config.py')

from .models import db
db.create_all()

from . import jinja2_addons
from . import views
from . import admin

from app.blueprints.auth import auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix="/auth")

from app.blueprints.forums import forum_blueprint
app.register_blueprint(forum_blueprint, url_prefix="/")

#from app.blueprints.submit import submit_blueprint
#app.register_blueprint(submit_blueprint, url_prefix="/submit")

