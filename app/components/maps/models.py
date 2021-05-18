#
# Sqlite3 with Flask:
#  https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
# SpatialLite with Geoalchemy2
#  https://geoalchemy-2.readthedocs.io/en/latest/spatialite_tutorial.html
# Managing Geographical Models in Flask-Admin
#  https://flask-admin.readthedocs.io/en/latest/advanced/
#

from sqlalchemy.engine import Engine
from sqlalchemy import event, func
from geoalchemy2.types import Geometry
import json
from app.models import db

@event.listens_for(Engine, "connect")
def sqlite_connect_hook(dbapi_connection, connection_record):

	# Load Spatialite extension
	dbapi_connection.enable_load_extension(True)
	dbapi_connection.load_extension('mod_spatialite')
	dbapi_connection.enable_load_extension(False)

	# Initialize the spatial extensions
	dbapi_connection.execute("SELECT InitSpatialMetaData(1)")

class Maps(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	description = db.Column(db.String)
	points = db.relationship('MapPoints')
	def __str__(self):
		return self.name

class MapPoints(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	map_id = db.Column(db.Integer, db.ForeignKey('maps.id'))
	map = db.relationship(Maps)
	name = db.Column(db.String)
	description = db.Column(db.String)
	comment = db.Column(db.String)
	source = db.Column(db.String)
	symbol = db.Column(db.String)
	geom = db.Column(Geometry(geometry_type='POINT', management=True))

	def as_geojson(self):
		print(self.geom)
		print(db.session.scalar(func.ST_AsGeoJSON(self.geom)))
		waypoint = json.loads(db.session.scalar(func.ST_AsGeoJSON(self.geom)))
		waypoint['properties'] = dict(
			name = self.name,
			description = self.description,
			)
		return waypoint

