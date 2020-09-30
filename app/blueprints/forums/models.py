from datetime import datetime
from app.models import db
from app.blueprints.auth import current_user
from app.blueprints.auth.models import Users

#=============================================================================
# We can run multiple forums on this server
#=============================================================================

class Forums(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)
	description = db.Column(db.String)
	creation_date = db.Column(db.DateTime, default=datetime.now)
	topics = db.relationship('Topics', back_populates="forum", lazy='dynamic', cascade='all')

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

	# Forum to which this topic belongs
	forum_id = db.Column(db.Integer, db.ForeignKey('forums.id'))
	forum = db.relationship("Forums", back_populates="topics")

	# User who created this topic
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=lambda: current_user.id)
	user = db.relationship(Users, back_populates="topics")

	# Topic headline, body, and metadata
	title = db.Column(db.String, nullable=False, unique=False)
	body = db.Column(db.Text, nullable=False)
	tags = db.relationship('TopicTags', secondary=topic_tags_rel, back_populates="topics")
	creation_date = db.Column(db.DateTime, default=datetime.now)
	edited_date = db.Column(db.DateTime)

	# Comments which users have posted on this topic
	comments = db.relationship("Comments", back_populates="topic", lazy='dynamic', cascade='all')

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

	# Topic to which this comment belongs
	topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"))
	topic = db.relationship(Topics, back_populates="comments")

	# User who posted this comment
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=lambda: current_user.id)
	user = db.relationship(Users, back_populates="comments")

	# Comment to which this person was replying or None
	reply_to_id = db.Column(db.Integer)

	# Comment body and metadata
	creation_date = db.Column(db.DateTime, default=datetime.now)
	edited_date = db.Column(db.DateTime)
	body = db.Column(db.Text)

	def __str__(self):
		return self.text

