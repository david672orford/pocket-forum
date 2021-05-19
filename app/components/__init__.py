import os
import logging
from importlib import import_module
from app import app

logger = logging.getLogger(__name__)

component_list = ["forum", "chat", "assignments", "maps", "users"]

def load_components():
	# From each component subdirectory load a Flask blueprint
	# and some Flask-Admin views.
	for component_name in component_list:
		logger.info("Importing blueprint for %s component..." % component_name)
		component_module = import_module("app.components.%s" % component_name)
		app.register_blueprint(component_module.blueprint, url_prefix="/%s" % component_name)
		import_module("app.components.%s.admin" % component_name)
