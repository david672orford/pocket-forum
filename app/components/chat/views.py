from flask import Blueprint, request, session, render_template, abort, redirect

blueprint = Blueprint('chat', __name__, template_folder="templates")

@blueprint.route("/")
def chat():
	return render_template("chat.html")

