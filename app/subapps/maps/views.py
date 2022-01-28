import logging
from flask import Blueprint, request, render_template
import xml.etree.ElementTree as ET
from .models import db, Maps, MapPoints

logger = logging.getLogger(__name__)

blueprint = Blueprint('maps', __name__, template_folder="templates")

@blueprint.route("/")
def map_index():
	return render_template("maps.html", maps = Maps.query.all())

def get_map(map_name):
	return Maps.query.filter_by(name=map_name).one()

@blueprint.route("/<map_name>")
def map_page(map_name):
    return render_template("map.html", map_obj=get_map(map_name))

@blueprint.route("/<map_name>/waypoints.geojson")
def waypoints(map_name):
	map_obj = get_map(map_name)
	points = map_obj.points
	return dict(
		type="FeatureCollection",
		features=[point.as_geojson() for point in points],
		)

@blueprint.route("/<map_name>/import.gpx", methods=['POST'])
def import_gpx(map_name):
	map_obj = get_map(map_name)
	root = ET.parse(request.stream).getroot()
	for child in root.findall("{http://www.topografix.com/GPX/1/1}wpt"):
		point = MapPoints(
			map_id = map_obj.id,
			name = child.findtext("{http://www.topografix.com/GPX/1/1}name"),
			description = child.findtext("{http://www.topografix.com/GPX/1/1}desc"),
			comment = child.findtext("{http://www.topografix.com/GPX/1/1}cmt"),
			symbol = child.findtext("{http://www.topografix.com/GPX/1/1}sym"),
			source = child.findtext("{http://www.topografix.com/GPX/1/1}src"),
			geom = 'POINT(%s %s)' % (float(child.get("lon")), float(child.get("lat"))),
			)
		db.session.add(point)
	db.session.commit()
	return "OK"


