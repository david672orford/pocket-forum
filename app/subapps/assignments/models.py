from app.models import db
from app.components.users import current_user
from app.components.users.models import Users

# An assignment which a teacher gives to a class
class Assignments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=lambda: current_user.id)
	user = db.relationship(Users)
	text = db.Column(db.Text, nullable=False)
	attachments = db.relationship('AssignmentsAttachments')

# A file which a teacher attaches to an assignment
class AssignmentsAttachments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
	name = db.Column(db.String, nullable=False, unique=True)
	mimetype = db.Column(db.String)

# A student's work turned in in fufillment of the assignment
class AssignmentsSubmissions(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=lambda: current_user.id)
	user = db.relationship(Users)
	text = db.Column(db.Text, nullable=False)
	attachments = db.relationship('AssignmentsSubmissionsAttachments')

# A file which a student attaches as part of the work he is handing in
class AssignmentsSubmissionsAttachments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	assignment_id = db.Column(db.Integer, db.ForeignKey('assignments_submissions.id'))
	name = db.Column(db.String, nullable=False, unique=True)
	mimetype = db.Column(db.String)
