from flask_admin import Admin
from flask_admin.contrib.sqla.view import ModelView as InsecureModelView
from flask_admin.form import SecureForm
from .models import db, Users, UserLinks, Forums, Topics, TopicTags, Comments
from . import app

def format_list(view, context, model, name):
	value = getattr(model, name)
	return ", ".join(map(str, value))

# Create base model view
class ModelView(InsecureModelView):
    form_base_class = SecureForm
    action_disallowed_list = ['delete']     # no mass delete
    page_size = 15

# Base model view with support for the HTML editor field
class HtmlModelView(ModelView):
    load_html_editor = True

# List of forums
class ForumsView(ModelView):
	column_list = ('name', 'description', 'creation_date')	
	form_columns = ('name', 'description')	

# List of all topics in all forums
class TopicsView(ModelView):
	column_list = ('forum', 'user', 'creation_date', 'title', 'tags')
	form_columns = ('forum', 'user', 'title', 'tags', 'body')
	form_widget_args = {
		'title': { 'class': 'wide' },
		'url': { 'class': 'wide' },
		}
	#inline_models = (Comments,)

# List of all available tags for topics
class TopicTagsView(ModelView):
	column_list = ('name',)
	form_columns = ('name',)

# List of all comments on all topics in all forums
class CommentsView(ModelView):
	column_list = ('topic', 'user', 'creation_date')
	form_columns = ('topic', 'user', 'body')

# List of all users
class UsersView(ModelView):
	column_list = ('handle', 'email', 'creation_date', 'links')
	form_columns = ('handle', 'email', 'links')
	inline_models = (UserLinks,)
	column_formatters = {'links': format_list}

admin = Admin(app, name=app.config['APP_DISPLAY_NAME'])
admin.add_view(ForumsView(Forums, db.session))
admin.add_view(TopicsView(Topics, db.session))
admin.add_view(CommentsView(Comments, db.session))
admin.add_view(TopicTagsView(TopicTags, db.session))
admin.add_view(UsersView(Users, db.session))

