from app.models import db
from app.blueprints.auth import current_user
from app.blueprints.auth.models import Users

class Boxes(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=lambda: current_user.id)
	user = db.relationship(Users) #, back_populates="boxes")

class Assignments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=lambda: current_user.id)
	user = db.relationship(Users) #, back_populates="assignments")
	name = db.Column(db.String, nullable=False)
	text = db.Column(db.Text, nullable=False)
	__table_args__ = (db.UniqueConstraint('user_id', 'name'),)
	
