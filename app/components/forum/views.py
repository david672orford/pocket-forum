from flask import Blueprint, request, session, render_template, abort, redirect
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

from .models import db, Users, ForumSections, ForumTopics, ForumComments
from app.forms import MyBaseForm, NameField, SubjectField, BodyField
from app.components.auth import current_user, login_required

#=============================================================================
# Database fetch
#=============================================================================

def get_section(section_name):
	try:
		forum = ForumSections.query.filter_by(name=section_name).one()
	except NoResultFound:
		abort(404)
	return forum

def get_topic(section, topic_id):
	try:
		topic = section.topics.filter_by(id=topic_id).one()
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
# Hierarcy: Forum -> Topic -> Comment
#=============================================================================

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

blueprint = Blueprint('forum', __name__, template_folder="templates")

# List forum sections
@blueprint.route("/")
def index():
	return render_template(
		"index.html",
		sections=ForumSections.query
		)

# List topics in a forum
@blueprint.route("/<section_name>/")
def section(section_name):
	section = get_section(section_name)
	return render_template("section.html", section=section)

# Topic Create
@blueprint.route("/<section_name>/new", methods=["GET","POST"])
@login_required
def topic_new(section_name):
	section = get_section(section_name)
	form = TopicForm(formdata=request.form)

	if request.method == 'POST' and form.validate():
		topic = ForumTopics(section=section)
		form.populate_obj(topic)
		db.session.add(topic)
		db.session.commit()
		# go to new topic page
		return redirect("%d" % topic.id)

	return render_template(
		"topic_editor.html",
		form=form,
		section=section,
		topic=None,
		)

# Topic Edit
@blueprint.route("/<section_name>/<int:topic_id>/editor", methods=['GET','POST'])
@login_required
def topic_edit(section_name, topic_id):
	section = get_section(section_name)
	topic = get_topic(section, topic_id)

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
		section=section,
		topic=topic,
		)

# Topic Delete
@blueprint.route("/<section_name>/<int:topic_id>/delete", methods=["GET", "POST"])
@login_required
def topic_delete(section_name, topic_id):
	section = get_section(section_name)
	topic = get_topic(section, topic_id)

	if topic.user != current_user:
		abort(403)

	form = DeleteForm(formdata=request.form)

	if request.method == "POST" and form.validate():
		db.session.delete(topic)
		db.session.commit()
		# go to section page
		return redirect("..")

	return render_template(
		"topic_delete.html",
		form=form,
		section=section,
		topic=topic
		)

# Topic View
@blueprint.route("/<section_name>/<int:topic_id>/")
def topic_view(section_name, topic_id):
	section = get_section(section_name)
	topic = get_topic(section, topic_id)

	return render_template(
		"topic.html",
		section=section,
		topic=topic,
		)

# Comment Create
@blueprint.route("/<section_name>/<int:topic_id>/new", methods=["GET", "POST"])
@login_required
def comment_new(section_name, topic_id):
	section = get_section(section_name)
	topic = get_topic(section, topic_id)
	form = CommentForm(formdata=request.form)

	if request.method == "POST" and form.validate():
		comment = ForumComments(topic=topic)
		form.populate_obj(comment)
		db.session.add(comment)
		db.session.commit()
		# go to topic page and scroll to new comment
		return redirect(".#c%d" % comment.id)

	return render_template(
		"comment_editor.html",
		form=form,
		section=section,
		topic=topic,
		comment=None
		)

# Comment Edit
@blueprint.route("/<section_name>/<int:topic_id>/<int:comment_id>/editor", methods=["GET", "POST"])
@login_required
def comment_edit(section_name, topic_id, comment_id):
	section = get_section(section_name)
	topic = get_topic(section, topic_id)
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
		section=section,
		topic=topic,
		comment=comment
		)

# Comment Delete
@blueprint.route("/<section_name>/<int:topic_id>/<int:comment_id>/delete", methods=["GET", "POST"])
@login_required
def comment_delete(section_name, topic_id, comment_id):
	section = get_section(section_name)
	topic = get_topic(section, topic_id)
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
		section=section,
		topic=topic,
		comment=comment
		)

