from datetime import datetime
from app.models import db

class AnonymousUser(object):
	id = None
	@property
	def is_authenticated(self):
		return False
	def __eq__(self, other):
		return self.id == other.id

# Tie user records to identities vouched for by authentication providers such
# as Google and Facebook
class UserLinks(db.Model, AnonymousUser):
	id = db.Column(db.Integer, primary_key=True)

	# Name of the identity provider
	idp = db.Column(db.String)

	# Unique token by which this provider identifies the user
	idp_id = db.Column(db.String)

	# The name by which the user is known on the identity provider's platform
	idp_display_name = db.Column(db.String)

	# Connection to the user's record in this forum
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	user = db.relationship('Users', back_populates="links")

	def __str__(self):
		return "{idp}:{idp_id} ({idp_display_name})".format(
			idp=self.idp,
			idp_id=self.idp_id,
			idp_display_name=self.idp_display_name,
			)

# The user record
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	# The name by which the user is known in the forum
	handle = db.Column(db.String, nullable=False)

	# Address at which user should receive notifications
	email = db.Column(db.String, nullable=True)

	# Date user created
	creation_date = db.Column(db.DateTime, default=datetime.now)

	# Topics opened by this user
	topics = db.relationship('Topics', back_populates="user", lazy='dynamic')

	# Comments posted by this user
	comments = db.relationship('Comments', back_populates="user", lazy='dynamic')

	# Links to identity providers
	links = db.relationship(UserLinks, back_populates="user", lazy='dynamic')

	def __str__(self):
		return "{handle} <{email}>".format(handle=self.handle, email=self.email)

	@property
	def is_authenticated(self):
		return True

