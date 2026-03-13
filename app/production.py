from werkzeug.middleware.proxy_fix import ProxyFix
from wsgi_door.providers import init_providers
from wsgi_door.middleware import WsgiDoorAuth, WsgiDoorFilter
import logging

from . import app, start_background

logger = logging.getLogger(__name__)
logger.info("Wrapping app in WSGI-Door")

app.wsgi_app = WsgiDoorFilter(
	app.wsgi_app,
	protected_paths = ["/admin/"],
	allowed_groups = app.config["ALLOWED_GROUPS"]
	)
app.wsgi_app = WsgiDoorAuth(
	app.wsgi_app,
	init_providers(app.config["AUTH_CLIENT_KEYS"]),
	app.config["SECRET_KEY"]
	)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_for=1)

start_background()
