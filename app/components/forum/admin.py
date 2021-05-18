from .models import db, ForumSections, ForumTopics, ForumTags, ForumComments
from app.admin import admin, ModelView

# List of forums
class ForumSectionsView(ModelView):
	list_columns = ('name', 'description', 'creation_date')	
	form_columns = ('name', 'description')	

# List of all topics in all forums
class ForumTopicsView(ModelView):
	list_columns = ('section', 'title', 'tags', 'user', 'creation_date')
	form_columns = ('section', 'title', 'tags', 'user', 'body')
	form_widget_args = {
		'title': { 'class': 'wide' },
		'url': { 'class': 'wide' },
		}
	#inline_models = (Comments,)

# List of all available tags for topics
class ForumTagsView(ModelView):
	column_list = ('name',)
	form_columns = ('name',)

# List of all comments on all topics in all forums
class ForumCommentsView(ModelView):
	column_list = ('topic', 'user', 'creation_date')
	form_columns = ('topic', 'user', 'body')

admin.add_view(ForumSectionsView(ForumSections, db.session, category="Forum"))
admin.add_view(ForumTopicsView(ForumTopics, db.session, category="Forum"))
admin.add_view(ForumCommentsView(ForumComments, db.session, category="Forum"))
admin.add_view(ForumTagsView(ForumTags, db.session, category="Forum"))

