from .models import db, ForumSections, ForumTopics, ForumTags, ForumComments
from app.admin import admin, ModelView

# List of forums
class ForumSectionsView(ModelView):
	column_list = ('name', 'description', 'creation_date')	
	form_columns = ('name', 'description')	

# List of all topics in all forums
class ForumTopicsView(ModelView):
	column_list = ('section', 'user', 'creation_date', 'title', 'tags')
	form_columns = ('section', 'user', 'title', 'tags', 'body')
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

