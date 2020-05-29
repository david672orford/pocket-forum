from flask import render_template
from . import app
from .models import db, Forums, Topics

@app.route("/")
def forums_list():
	return render_template("index.html", title="Forums", forums=Forums.query)

@app.route("/<forum_name>/")
def forum(forum_name):
	forum=Forums.query.filter_by(name=forum_name).one()
	return render_template("forum.html", title=forum.name, forum=forum)

@app.route("/<forum_name>/<int:topicid>")
def forum_topic(forum_name, 
	topic=Topics.query.filter_by(id=topicid).one()
	assert topic.forum.name == forum_name
	return render_template("forum_topic.html", topic=topic)

