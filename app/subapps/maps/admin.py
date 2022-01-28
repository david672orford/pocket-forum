from .models import db, Maps, MapPoints
from app.admin import admin, ModelView

class MapsView(ModelView):
	list_columns = ('name', 'description')
	form_columns = list_columns

class MapPointsView(ModelView):
	list_columns = ('map', 'symbol', 'name', 'description')
	form_columns = list_columns + ('comment', 'source', 'geom')

admin.add_view(MapsView(Maps, db.session, endpoint="_maps", category="Maps"))
admin.add_view(MapPointsView(MapPoints, db.session, category="Maps"))

