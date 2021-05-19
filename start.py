#! /usr/bin/python3

import sys
sys.path.append("../../Modules/wsgi_door")
import logging
#from werkzeug.serving import run_simple
from werkzeug.middleware.proxy_fix import ProxyFix
from app import app, load_components
from app.socketio import socketio

debug_mode = (len(sys.argv) >= 2 and sys.argv[1] == '--debug')
logging.basicConfig(level=logging.DEBUG if debug_mode else logging.INFO)

load_components()

if not debug_mode:
	from wsgi_door.providers import init_providers
	from wsgi_door.middleware import WsgiDoorAuth, WsgiDoorFilter
	app.wsgi_app = WsgiDoorFilter(app.wsgi_app, protected_paths=["/admin/"], allowed_groups=app.config['ALLOWED_GROUPS'])
	auth_providers = init_providers(app.config['AUTH_CLIENT_KEYS'])
	app.wsgi_app = WsgiDoorAuth(app.wsgi_app, auth_providers, app.config['SECRET_KEY'], stylesheet_url="/static/base.css")

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_for=1)
#run_simple('0.0.0.0', 5000, app)
socketio.run(app, debug=True)
