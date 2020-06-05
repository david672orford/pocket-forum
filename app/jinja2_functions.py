from time import time
from app import app

def format_datetime(the_datetime):
	return "%d-%02d-%2d %02d:%02d" % (the_datetime.year, the_datetime.month, the_datetime.day, the_datetime.hour, the_datetime.minute)
app.jinja_env.filters['datetime'] = format_datetime

def format_when(the_datetime):
	if the_datetime is None:
		return "-"

	seconds_ago = int(time() - the_datetime.timestamp())
	if seconds_ago < 120:
		return "%d seconds ago" % seconds_ago

	minutes_ago = int((seconds_ago + 30) / 60)
	if minutes_ago < 120:
		return "%d minutes ago" % minutes_ago

	hours_ago = int((minutes_ago + 30) / 60)
	if hours_ago < 48:
		return "%d hours ago" % hours_ago

	days_ago = int((hours_ago + 12) / 24)
	if days_ago < 7:
		return "%d days ago" % days_ago

	weeks_ago = int((days_ago + 3) / 7)
	if weeks_ago < 4:
		return "%d weeks ago" % weeks_ago

	months_ago = int((days_ago + 14) / 30)
	if months_ago < 24:
		return "%d months ago" % months_ago

	years_ago = int((months_ago + 6) / 12)
	return "%d years ago" % years_ago

app.jinja_env.filters['when'] = format_when

