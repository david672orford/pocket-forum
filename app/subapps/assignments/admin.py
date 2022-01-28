from .models import db, Assignments, AssignmentsAttachments, AssignmentsSubmissions, AssignmentsSubmissionsAttachments
from app.admin import admin, ModelView

class AssignmentsView(ModelView):
    list_columns = ("user", "name")
    form_columns = ("user", "name", "text", "attachments")

class AssignmentsAttachmentsView(ModelView):
    pass

class AssignmentsSubmissionsView(ModelView):
    pass

class AssignmentsSubmissionsAttachmentsView(ModelView):
    pass

admin.add_view(AssignmentsView(Assignments, db.session, category="Assignments"))
admin.add_view(AssignmentsAttachmentsView(AssignmentsAttachments, db.session, url="assignments-attachements", category="Assignments"))
admin.add_view(AssignmentsSubmissionsView(AssignmentsSubmissions, db.session, url="assignments-submissions", category="Assignments"))
admin.add_view(AssignmentsSubmissionsAttachmentsView(AssignmentsSubmissionsAttachments, db.session, url="assignments-submissions-attachments", category="Assignments"))
