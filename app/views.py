# Views which are not part of a component

from flask import abort, redirect

from . import app

@app.route("/")
def index():
	return redirect("/admin/")

@app.route("/favicon.ico")
def favicon():
	abort(404)

