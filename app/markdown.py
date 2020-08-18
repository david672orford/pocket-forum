import markdown
from lxml.html.clean import Cleaner
from jinja2 import Markup

from app import app

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

