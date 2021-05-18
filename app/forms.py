from wtforms import Form, StringField, TextAreaField
from wtforms.csrf.session import SessionCSRF
from wtforms.validators import DataRequired

# Because we are not using Flask-WTF we must enable CSRF ourselves.
class MyBaseForm(Form):
	class Meta:
		csrf = True
		csrf_class = SessionCSRF

		@property
		def csrf_secret(self):
			return app.secret_key

		@property
		def csrf_context(self):
			return session

# Add features to WTForms field:
# * placeholder option
# * strip whitespace from ends
class MyFieldMixin(object):
	def __init__(self, placeholder=None, **kwargs):
		super().__init__(validators=[DataRequired()], render_kw={'placeholder':placeholder}, **kwargs)
	def populate_obj(self, obj, name):
		setattr(obj, name, self.data.strip())

# Short name
class NameField(MyFieldMixin, StringField):
	pass

# One-line description
class SubjectField(MyFieldMixin, StringField):
	pass

# Body of message
class BodyField(MyFieldMixin, TextAreaField):
	pass


