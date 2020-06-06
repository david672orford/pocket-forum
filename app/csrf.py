# References:
# https://github.com/lepture/flask-wtf/blob/master/flask_wtf/csrf.py
# https://github.com/sjl/flask-csrf/blob/master/flaskext/csrf.py

from flask import session, request, g
from itsdangerous import BadData, SignatureExpired, URLSafeTimedSerializer
from werkzeug.exceptions import BadRequest
from werkzeug.security import safe_str_cmp
from secrets import token_urlsafe
from markupsafe import Markup, escape

def csrf_protect(app):

	# Used for signing the copy of the token stored in a hidden field of the form
	serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'], salt='csrf-protection')

	@app.before_request
	def csrf_before_request():
		if request.method == 'POST':

			if not '_csrf_token' in request.form:
				raise BadRequest("No CSRF token in form")

			if not '_csrf_token' in session:
				raise BadRequest("No CSRF token in session")

			try:
				form_token = serializer.loads(request.form['_csrf_token'], max_age=3600)
			except BadData:
				raise BadRequest("CSRF token invalid")
			except SignatureExpired:
				raise BadRequest("CSRF token expired")

			if not safe_str_cmp(session['_csrf_token'], form_token):
				raise BadRequest("CSRF token mismatch")

		return None

	def csrf_field():
		if not '_csrf_token' in g:
			token = token_urlsafe()
			session['_csrf_token'] = token
			g._csrf_token = serializer.dumps(token)
		return Markup('<input type="hidden" name="_csrf_token" value="%s">' % escape(g._csrf_token))
	app.jinja_env.globals['csrf_field'] = csrf_field

