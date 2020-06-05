from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.engine import Engine
from sqlalchemy import event

db = SQLAlchemy(app)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
	cursor = dbapi_connection.cursor()
	cursor.execute("PRAGMA foreign_keys=ON")
	cursor.close()

#=============================================================================
# Users
#=============================================================================

# Tie user records to identities vouched for by authentication providers such
# as Google and Facebook
class UserLinks(db.Model):
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
	email = db.Column(db.String, nullable=False)

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

#=============================================================================
# We can run multiple forums on this server
#=============================================================================

class Forums(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)
	description = db.Column(db.String)
	creation_date = db.Column(db.DateTime, default=datetime.now)
	topics = db.relationship("Topics", back_populates="forum", lazy='dynamic')

	def __str__(self):
		return self.name

#=============================================================================
# Discussion topics and their tags
#=============================================================================

topic_tags_rel = db.Table("topic_tags_rel", db.Model.metadata,
	db.Column('id', db.Integer, primary_key=True),
	db.Column('topic_id', db.Integer, db.ForeignKey('topics.id')),
	db.Column('topic_tags_id', db.Integer, db.ForeignKey('topic_tags.id'))
	)

class Topics(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	forum_id = db.Column(db.Integer, db.ForeignKey('forums.id'))
	forum = db.relationship("Forums", back_populates="topics")
	title = db.Column(db.String, nullable=False, unique=False)
	tags = db.relationship('TopicTags', secondary=topic_tags_rel, back_populates="topics")
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	user = db.relationship(Users, back_populates="topics")
	creation_date = db.Column(db.DateTime, default=datetime.now)
	body = db.Column(db.Text)
	comments = db.relationship("Comments", back_populates="topic", lazy='dynamic')
	def __str__(self):
		return self.title

class TopicTags(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)
	topics = db.relationship(Topics, secondary=topic_tags_rel, back_populates="tags")
	def __str__(self):
		return self.name

#=============================================================================
# Comments on articles
#=============================================================================

class Comments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"))
	topic = db.relationship(Topics, back_populates="comments")
	reply_to_id = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	user = db.relationship(Users, back_populates="comments")
	creation_date = db.Column(db.DateTime, default=datetime.now)
	body = db.Column(db.Text)
	def __str__(self):
		return self.text

db.create_all()

