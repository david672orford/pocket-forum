import logging
from flask import Blueprint, render_template
from .models import db, Users, UserLinks, AnonymousUser

logger = logging.getLogger(__name__)

blueprint = Blueprint('auth', __name__, template_folder="templates")

# Passed through from WSGI_Door when the user logs out
@blueprint.route("/logout")
def logout_hook():
	logger.debug("logout hook")
	logout_user()
	return ""			# no body required

# User profile
@blueprint.route("/profile")
@login_required
def profile():
	return render_template("profile.html")
