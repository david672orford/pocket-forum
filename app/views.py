from flask import request, render_template, abort, redirect
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

from . import app
from .models import db, Users, Forums, Topics, Comments
from .login import current_user, login_required

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
		comment = topic.filter_by(id=comment_id).one()
	except NoResultFound:
		abort(404)
	return comment

# List forums
@app.route("/")
def forums_list():
	return render_template("index.html", title="Forums", forums=Forums.query)

# List topics in a forum
@app.route("/<forum_name>/")
def forum(forum_name):
	forum = get_forum(forum_name)
	return render_template("forum.html", title=forum.name, forum=forum)

# Create a new topic in one of the forums
@login_required
@app.route("/<forum_name>/new", methods=["GET","POST"])
def topic_new(forum_name):
	forum = get_forum(forum_name)

	if request.method == "POST":
		title = request.form['title'].strip()
		body = request.form['body'].strip()
		if title and body:
			topic = Topics(
				forum=forum,
				user_id=current_user.id,
				title=title,
				body=title,
				)
			db.session.add(topic)
			db.session.commit()
			return redirect("%d" % topic.id)

	return render_template("topic_new.html", title="%s: New Topic" % forum.name)

# Show an existing topic from one of the forums
@app.route("/<forum_name>/<int:topic_id>", methods=['GET','POST'])
def topic(forum_name, topic_id):
	forum = get_forum(forum_name)
	topic = get_topic(forum, topic_id)

	if request.method == 'GET':
		return render_template(
			"topic.html",
			title="%s: %s" % (forum.name, topic.title),
			topic=topic,
			current_user=current_user,
			)

	topic.title = request.form['title']
	topic.body = request.form['body']
	topic.edited_date = datetime.now()
	db.session.commit()
	return redirect("%d" % topic.id)

# Create a new comment on a forum topic
@login_required
@app.route("/<forum_name>/<int:topic_id>/new", methods=["GET", "POST"])
def comment_new(forum_name, topic_id):
	forum = get_forum(forum_name)
	topic = get_topic(forum, topic_id)

	if request.method == "GET":
		return render_template("comment_new.html", title="%s: %s: New Comment" % (forum.name, topic.title))

	body = request.form['body'].strip()
	if body:
		comment = Comments(
			topic=topic,
			user_id=current_user.id,
			body=body,
			)
		db.session.add(comment)
		db.session.commit()
	return redirect("../%d#c%d" % (topic.id, comment.id))

# Edit a comment on a forum topic
@login_required
@app.route("/<forum_name>/<int:topic_id>/<int:comment_id>", methods=["GET", "POST"])
def comment(forum_name, topic_id, comment_id):
	forum = get_forum(forum_name)
	topic = get_topic(forum, topic_id)
	comment = get_comment(topic, comment_id)

	if request.method == "GET":
		return render_template("comment_edit.html", title="%s: %s: Edit Comment" % (forum.name, topic.title), comment=comment)

	comment.body = request.form.body
	comment.edited_date = datetime.now()
	db.session.commit()
	return redirect("../%d#c%d" % (topic.id, comment.id))

