from flask import Blueprint, request, session, render_template, abort, redirect

from .models import db, Assignments, AssignmentsAttachments, AssignmentsSubmissions, AssignmentsSubmissionsAttachments
from app.forms import MyBaseForm, NameField, SubjectField, BodyField
from app.components.users import current_user, login_required

#=============================================================================
# Forms
#=============================================================================

class AssignmentForm(MyBaseForm):
	name = NameField(placeholder='Name of Assignment')
	body = BodyField(placeholder='Please describe the assignment')

#=============================================================================
# Content Views
#=============================================================================

blueprint = Blueprint('submit', __name__, template_folder="templates")

@blueprint.route("/")
def index():
	return render_template(
		"index.html",
		assignments=Assignments.query
		)

@blueprint.route("/new", methods=["GET","POST"])
@login_required
def assignment_new():
	form = AssignmentForm(formdata=request.form)

	if request.method == 'POST' and form.validate():
		assignment = Assignment()
		form.populate_obj(assignment)
		db.session.add(assignment)
		db.session.commit()
		return redirect("%d" % assignment.id)

	return render_template(
		"assignment_editor.html",
		form=form,
		section=section,
		topic=None,
		)

@blueprint.route("/<int:assignment_id>/")
@login_required
def assignment(assignment_id):
	return render_template(
		"assignment.html",
		assignment=Assignments.query.filter_by(id=assignment_id).one()
		)

@blueprint.route("/<int:assignment_id>/new", methods=["GET","POST"])
@login_required
def submission_new(assignment_id):
	return render_template(
		"submission_new.html",
		assignment=Assignments.query.filter_by(id=assignment_id).one()
		)

@blueprint.route("/<int:assignment_id>/<int:submission_id>", methods=["GET","POST"])
@login_required
def submission(assignment_id, submission_id):
	assignment = Assignments.query.filter_by(id=assignment_id).one()
	submission = assignment.submissions.filter_by(id=submission_id).one()
	return render_template(
		"submission.html",
		submission=submission
		)
