from .models import db, Users, UserLinks
from app.admin import admin, ModelView

def format_list(view, context, model, name):
	value = getattr(model, name)
	return ", ".join(map(str, value))

class UsersView(ModelView):
	column_list = ('handle', 'email', 'creation_date', 'links')
	form_columns = ('handle', 'email', 'links')
	inline_models = (UserLinks,)
	column_formatters = {'links': format_list}

admin.add_view(UsersView(Users, db.session))

