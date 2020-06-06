from time import time
from app import app

def format_datetime(the_datetime):
	return "%d-%02d-%02d %02d:%02d" % (the_datetime.year, the_datetime.month, the_datetime.day, the_datetime.hour, the_datetime.minute)
app.jinja_env.filters['datetime'] = format_datetime

