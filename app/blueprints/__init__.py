import os
from importlib import import_module
from app import app

blueprint_names = []
for blueprint_name in filter(lambda bp: not bp.startswith("__"), os.listdir("app/blueprints")):
	print("Importing %s blueprint..." % blueprint_name)

	blueprint_module = import_module("app.blueprints.%s" % blueprint_name)
	app.register_blueprint(blueprint_module.blueprint, url_prefix="/%s" % blueprint_name)

	blueprint_names.append(blueprint_name)

for blueprint_name in blueprint_names:
	import_module("app.blueprints.%s.admin" % blueprint_name)


