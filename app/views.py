from flask import request, render_template, abort, redirect
from sqlalchemy.orm.exc import NoResultFound
from . import app
from .models import db, Users, Forums, Topics, Comments

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

# List forums
@app.route("/")
def forums_list():
	return render_template("index.html", title="Forums", forums=Forums.query)

# List topics in a forum
@app.route("/<forum_name>/")
def forum(forum_name):
	forum = get_forum(forum_name)
	return render_template("forum.html", title=forum.name, forum=forum)

# Create a new topic in a forum
@app.route("/<forum_name>/new", methods=["GET","POST"])
def forum_topic_new(forum_name):
	forum = get_forum(forum_name)
	if request.method == "GET":
		return render_template("forum_topic_new.html", title="%s: New Topic" % forum.name)
	topic = Topics(
		forum = forum,
		user = Users.query.filter_by(handle="joe").one(),
		title = request.form['title'],
		body = request.form['body'],
		)
	db.session.add(topic)
	db.session.commit()
	return redirect("%d" % topic.id)

# Show a topic in a forum
@app.route("/<forum_name>/<int:topic_id>")
def forum_topic(forum_name, topic_id):
	forum = get_forum(forum_name)
	topic = get_topic(forum, topic_id)
	return render_template("forum_topic.html", title="%s: %s" % (forum.name, topic.title), forum=forum, topic=topic)

# Create a new comment on a forum topic
@app.route("/<forum_name>/<int:topic_id>/new", methods=["POST"])
def form_topic_comment_new(forum_name, topic_id):
	forum = get_forum(forum_name)
	topic = get_topic(forum, topic_id)
	comment = Comments(
		topic = topic,
		user = Users.query.filter_by(handle="joe").one(),
		body = request.form['body'],
		)
	db.session.add(comment)
	db.session.commit()
	return redirect("../%d" % topic.id)

