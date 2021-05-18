# Views which are not part of a component

from flask import abort, redirect, render_template

from . import app
from .components import component_list

@app.route("/")
def index():
	#return redirect("/admin/")
	return render_template("index.html", component_list=component_list)

@app.route("/favicon.ico")
def favicon():
	abort(404)

