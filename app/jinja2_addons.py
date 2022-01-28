from jinja2 import Markup

from app import app

#=============================================================================
# Date and Time
#=============================================================================

def format_datetime(the_datetime):
	return "%d-%02d-%02d %02d:%02d" % (the_datetime.year, the_datetime.month, the_datetime.day, the_datetime.hour, the_datetime.minute)
app.jinja_env.filters['datetime'] = format_datetime

#=============================================================================
# Login
#=============================================================================

from app.subapps.users import current_user
app.jinja_env.globals['current_user'] = current_user

#=============================================================================
# Convert Markdown to HTML
#=============================================================================

import markdown
from lxml.html.clean import Cleaner

markdown_processor = markdown.Markdown(extensions=['tables', 'codehilite', 'fenced_code', 'smarty'])

cleaner = Cleaner(
	allow_tags = (
		"a", "img",
		"h1", "h2", "h3",
		"strong", "em", "b", "i", "sub", "sup",
		"p", "br", "hr", "pre", "div",
		"ul", "ol", "li",
		"table", "thead", "tbody", "tr", "th", "td",
		),
	remove_unknown_tags = False,
	safe_attrs = set(["class", "href", "src", "alt"]),
	)

def format_markdown(text):
	html = markdown_processor.convert(text)
	html = cleaner.clean_html(html)
	return Markup(html)

app.jinja_env.filters['markdown'] = format_markdown
