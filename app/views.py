from flask import request, session, render_template, abort, redirect
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from wtforms import Form, StringField, TextAreaField
from wtforms.csrf.session import SessionCSRF
from wtforms.validators import DataRequired

from . import app
from .models import db, Users, Forums, Topics, Comments
from .login import current_user, login_required

#=============================================================================
# Database fetch
#=============================================================================

def get_forum(forum_name):
	try:
		forum = Forums.query.filter_by(name=forum_name).one()
	except NoResultFound:
		abort(404)
	return forum

def get_topic(forum, topic_id):
	try:
		topic = forum.topics.filter_by(id=topic_id).one()
	except NoResultFound:
		abort(404)
	return topic

def get_comment(topic, comment_id):
	try:
		comment = topic.comments.filter_by(id=comment_id).one()
	except NoResultFound:
		abort(404)
	return comment

#=============================================================================
# Forms
#=============================================================================

# Because we are not using Flask-WTF we must enable CSRF ourselves.
class MyBaseForm(Form):
	class Meta:
		csrf = True
		csrf_class = SessionCSRF

		@property
		def csrf_secret(self):
			return app.secret_key

		@property
		def csrf_context(self):
			return session

class MyFieldMixin(object):
	def __init__(self, placeholder=None, **kwargs):
		super().__init__(validators=[DataRequired()], render_kw={'placeholder':placeholder}, **kwargs)
	def populate_obj(self, obj, name):
		setattr(obj, name, self.data.strip())

class NameField(MyFieldMixin, StringField):
	pass

class SubjectField(MyFieldMixin, StringField):
	pass

class BodyField(MyFieldMixin, TextAreaField):
	pass

class ForumForm(MyBaseForm):
	name = NameField(placeholder='Forum Name')
	description = SubjectField(placeholder='Forum Description')

class TopicForm(MyBaseForm):
	title = SubjectField(placeholder='Topic Title')
	body = BodyField(placeholder='Topic Description')

class CommentForm(MyBaseForm):
	body = BodyField(placeholder='Your Comment')

class DeleteForm(MyBaseForm):
	pass

#=============================================================================
# Content Views
#=============================================================================

# List forums
@app.route("/")
def forums_list():
	return render_template(
		"index.html",
		forums=Forums.query
		)

@app.route("/favicon.ico")
def favicon():
	abort(404)

# List topics in a forum
@app.route("/<forum_name>/")
def forum(forum_name):
	forum = get_forum(forum_name)
	return render_template("forum.html", forum=forum)

# Topic Create
@app.route("/<forum_name>/new", methods=["GET","POST"])
@login_required
def topic_new(forum_name):
	forum = get_forum(forum_name)
	form = TopicForm(formdata=request.form)

	if request.method == 'POST' and form.validate():
		topic = Topics(forum=forum)
		form.populate_obj(topic)
		db.session.add(topic)
		db.session.commit()
		# go to new topic page
		return redirect("%d" % topic.id)

	return render_template(
		"topic_editor.html",
		form=form,
		forum=forum,
		topic=None,
		)

# Topic Edit
@app.route("/<forum_name>/<int:topic_id>/editor", methods=['GET','POST'])
@login_required
def topic_edit(forum_name, topic_id):
	forum = get_forum(forum_name)
	topic = get_topic(forum, topic_id)

	if topic.user != current_user:
		abort(403)

	form = TopicForm(formdata=request.form, obj=topic)

	if request.method == 'POST' and form.validate():
		print("Save topic...")
		form.populate_obj(topic)
		topic.edited_date = datetime.now()
		db.session.commit()
		# go back to topic page
		return redirect(".")

	return render_template(
		"topic_editor.html",
		form=form,
		forum=forum,
		topic=topic,
		)

# Topic Delete
@app.route("/<forum_name>/<int:topic_id>/delete", methods=["GET", "POST"])
@login_required
def topic_delete(forum_name, topic_id):
	forum = get_forum(forum_name)
	topic = get_topic(forum, topic_id)

	if topic.user != current_user:
		abort(403)

	form = DeleteForm(formdata=request.form)

	if request.method == "POST" and form.validate():
		db.session.delete(topic)
		db.session.commit()
		# go to forum page
		return redirect("..")

	return render_template(
		"topic_delete.html",
		form=form,
		forum=forum,
		topic=topic
		)

# Topic View
@app.route("/<forum_name>/<int:topic_id>/")
def topic_view(forum_name, topic_id):
	forum = get_forum(forum_name)
	topic = get_topic(forum, topic_id)

	return render_template(
		"topic.html",
		forum=forum,
		topic=topic,
		)

# Comment Create
@app.route("/<forum_name>/<int:topic_id>/new", methods=["GET", "POST"])
@login_required
def comment_new(forum_name, topic_id):
	forum = get_forum(forum_name)
	topic = get_topic(forum, topic_id)
	form = CommentForm(formdata=request.form)

	if request.method == "POST" and form.validate():
		comment = Comments(topic=topic)
		form.populate_obj(comment)
		db.session.add(comment)
		db.session.commit()
		# go to topic page and scroll to new comment
		return redirect(".#c%d" % comment.id)

	return render_template(
		"comment_editor.html",
		form=form,
		forum=forum,
		topic=topic,
		comment=None
		)

# Comment Edit
@app.route("/<forum_name>/<int:topic_id>/<int:comment_id>/editor", methods=["GET", "POST"])
@login_required
def comment_edit(forum_name, topic_id, comment_id):
	forum = get_forum(forum_name)
	topic = get_topic(forum, topic_id)
	comment = get_comment(topic, comment_id)

	if comment.user != current_user:
		abort(403)

	form = CommentForm(formdata=request.form, obj=comment)

	if request.method == "POST" and form.validate():
		form.populate_obj(comment)
		comment.edited_date = datetime.now()
		db.session.commit()
		# Go to topic page and scroll to edited comment
		return redirect("..#c%d" % comment.id)

	return render_template(
		"comment_editor.html",
		form=form,
		forum=forum,
		topic=topic,
		comment=comment
		)

# Comment Delete
@app.route("/<forum_name>/<int:topic_id>/<int:comment_id>/delete", methods=["GET", "POST"])
@login_required
def comment_delete(forum_name, topic_id, comment_id):
	forum = get_forum(forum_name)
	topic = get_topic(forum, topic_id)
	comment = get_comment(topic, comment_id)

	if comment.user != current_user:
		abort(403)

	form = DeleteForm(formdata=request.form)

	if request.method == "POST" and form.validate():
		db.session.delete(comment)
		db.session.commit()
		# Go to topic page
		return redirect("..")

	return render_template(
		"comment_delete.html",
		form=form,
		forum=forum,
		topic=topic,
		comment=comment
		)

