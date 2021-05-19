import logging
from flask import Blueprint, render_template, redirect
from .login import login_required, logout_user

logger = logging.getLogger(__name__)

blueprint = Blueprint('auth', __name__, template_folder="templates")

@blueprint.route("/")
def index():
	return redirect("profile")

# User profile
@blueprint.route("/profile")
@login_required
def profile():
	return render_template("profile.html")

# Passed through from WSGI_Door when the user logs out
@blueprint.route("/logout")
def logout_hook():
	logger.debug("logout hook")
	logout_user()
	return ""			# no body required
