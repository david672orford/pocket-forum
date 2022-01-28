# Views which are not part of a component

from flask import abort, redirect, render_template

from . import app

@app.route("/")
def index():
	#return redirect("/admin/")
	return render_template("index.html", subapps=app.config['ENABLED_SUBAPPS'])

@app.route("/favicon.ico")
def favicon():
	abort(404)

