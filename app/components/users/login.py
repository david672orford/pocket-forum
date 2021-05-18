import logging
from flask import redirect, request, g, session, render_template
from werkzeug.local import LocalProxy
from functools import wraps

logger = logging.getLogger(__name__)

# Implement current_user like in Flask-Login
def _get_user():
	logger.debug("_get_user: %s" % session.get('_user_id'))
	if not 'user' in g:
		user = None

		if '_user_id' in session:
			user = Users.query.filter_by(id=int(session['_user_id'])).first()
			logger.debug("user: %s" % user)

		if user is None:
			wsgi_door = request.environ.get('wsgi_door',{})
			if 'provider' in wsgi_door:
				# Look for a link between this social media login and one of our accounts
				user_link = UserLinks.query.filter_by(idp=wsgi_door['provider'], idp_id=wsgi_door['id']).first()

				# This social login is not linked to one of our accounts.
				if user_link is None:

					handle = wsgi_door['name']
					if handle is None:
						handle = wsgi_door['username']

					# Create user record copying data from the social login account
					user = Users(handle=handle, email=wsgi_door['email'])
					db.session.add(user)

					# Link the newly created user to the social login account
					user_link = UserLinks(user=user, idp=wsgi_door['provider'], idp_id=wsgi_door['id'], idp_display_name=wsgi_door['username'])
					db.session.add(user_link)

					db.session.commit()

				# This social login is linked to one of our accounts
				else:
					user = Users.query.filter_by(id=user_link.user_id).one()

				session['_user_id'] = user.id

		if user is None:
			user = AnonymousUser()

		g.user = user

	return g.user

current_user = LocalProxy(_get_user)

# Implement @login_required like in Flask-Login
def login_required(func):
	@wraps(func)
	def secure_function(*args, **kwargs):
		if not current_user.is_authenticated:
			response = redirect("/auth/login/")
			request.environ['wsgi_door'].set_next_url(response, request.url)
			return response
		return func(*args, **kwargs)
	return secure_function

# Implement logout_user() like in Flask-Login
def logout_user():
	session.pop('_user_id')
