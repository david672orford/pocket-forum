from flask import abort

from . import app

@app.route("/favicon.ico")
def favicon():
	abort(404)

