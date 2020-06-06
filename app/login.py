from flask import redirect
from flask_login import LoginManager, login_user, current_user, login_required
from .models import db, Users, UserLinks

login_manager = LoginManager()

# Called if the user is logged in at the LoginManager level
@login_manager.user_loader
def load_user(user_id):
	print("Load user")
	return Users.query.filter_by(id=int(user_id)).first()

# Called if the user is not logged in at the LoginManager level
@login_manager.request_loader
def request_load_user(request):
	print("Load user from request")	

	wsgi_door = request.environ['wsgi_door']

	if 'provider' in wsgi_door:
		user_link = UserLinks.query.filter_by(idp=wsgi_door['provider'], idp_id=wsgi_door['id']).first()
		if user_link is None:

			user = Users(handle=wsgi_door['name'], email=wsgi_door['email'])
			db.session.add(user)

			user_link = UserLinks(user=user, idp=wsgi_door['provider'], idp_id=wsgi_door['id'], idp_display_name=wsgi_door['username'])
			db.session.add(user_link)

			db.session.commit()

		else:
			user = Users.query.filter_by(id=user_link.user_id).one()

		login_user(user)
		return user

	return None

# User has hit a protected view while not logged in. Save the
# requested URL and send him to the login page.
@login_manager.unauthorized_handler
def unauthorized():
	response = redirect("/auth/login/")
	request.environ['wsgi_door'].set_next_url(response, request.url)
	return response

