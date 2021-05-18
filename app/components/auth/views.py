from flask import Blueprint, redirect, request, g, session, render_template
from werkzeug.local import LocalProxy
from functools import wraps

from .models import db, Users, UserLinks, AnonymousUser

blueprint = Blueprint('auth', __name__, template_folder="templates")

# Implement current_user like in Flask-Login
def _get_user():
	print("_get_user", session.get('_user_id'))
	if not 'user' in g:
		user = None

		if '_user_id' in session:
			user = Users.query.filter_by(id=int(session['_user_id'])).first()
			print("user:", user)

		if user is None:
			wsgi_door = request.environ['wsgi_door']
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

# Passed through from WSGI_Door when the user logs out
@blueprint.route("/logout")
def logout_hook():
	print("logout hook")
	session.pop('_user_id')
	return ""

# User profile
@blueprint.route("/profile")
@login_required
def profile():
	return render_template("profile.html")
 
