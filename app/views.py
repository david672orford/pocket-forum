from flask import render_template
from . import app
from .models import db, Forums

@app.route("/")
def forums_list():
	return render_template("forums.html", title="Forums", forums=Forums.query)

@app.route("/<name>")
def forums_show(name):
	forum=Forums.query.filter_by(name=name).one()
	return render_template("forum.html", title=forum.name, forum=forum)


