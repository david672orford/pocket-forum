from datetime import datetime
from app.models import db
from app.components.users import current_user
from app.components.users.models import Users

#=============================================================================
# Forum is divided into sections each of which contains topics
#=============================================================================

class ForumSections(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)
	description = db.Column(db.String)
	creation_date = db.Column(db.DateTime, default=datetime.now)
	topics = db.relationship('ForumTopics', back_populates="section", lazy='dynamic', cascade='all')

	def __str__(self):
		return self.name

#=============================================================================
# Discussion topics and their tags
#=============================================================================

tags_rel = db.Table("forum_tags_rel", db.Model.metadata,
	db.Column('id', db.Integer, primary_key=True),
	db.Column('topic_id', db.Integer, db.ForeignKey('forum_topics.id')),
	db.Column('topic_tags_id', db.Integer, db.ForeignKey('forum_tags.id'))
	)

class ForumTopics(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	# Forum to which this topic belongs
	section_id = db.Column(db.Integer, db.ForeignKey('forum_sections.id'))
	section = db.relationship("ForumSections", back_populates="topics")

	# User who created this topic
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=lambda: current_user.id)
	user = db.relationship(Users)

	# Topic headline, body, and metadata
	title = db.Column(db.String, nullable=False, unique=False)
	body = db.Column(db.Text, nullable=False)
	tags = db.relationship('ForumTags', secondary=tags_rel, back_populates="topics")
	creation_date = db.Column(db.DateTime, default=datetime.now)
	edited_date = db.Column(db.DateTime)

	# Comments which users have posted on this topic
	comments = db.relationship("ForumComments", back_populates="topic", lazy='dynamic', cascade='all')

	def __str__(self):
		return self.title

class ForumTags(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)
	topics = db.relationship(ForumTopics, secondary=tags_rel, back_populates="tags")
	def __str__(self):
		return self.name

#=============================================================================
# Comments on articles
#=============================================================================

class ForumComments(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	# Topic to which this comment belongs
	topic_id = db.Column(db.Integer, db.ForeignKey("forum_topics.id"))
	topic = db.relationship(ForumTopics, back_populates="comments")

	# User who posted this comment
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=lambda: current_user.id)
	user = db.relationship(Users)

	# Comment to which this person was replying or None
	reply_to_id = db.Column(db.Integer)

	# Comment body and metadata
	creation_date = db.Column(db.DateTime, default=datetime.now)
	edited_date = db.Column(db.DateTime)
	body = db.Column(db.Text)

	def __str__(self):
		return self.text
