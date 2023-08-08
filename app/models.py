from sqlalchemy.sql import func
from app.exts import db

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	verified = db.Column(db.Boolean, default=False)

	def __init__(self, email, password, verified):
		self.email = email
		self.password = password
		self.verified = verified

class Task(db.Model):
	__tablename__ = 'tasks'

	id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.String(255), unique=True, nullable=False)
	complete = db.Column(db.Boolean, nullable=True, default=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	created_at = db.Column(
		db.DateTime(timezone=True),
		server_default=func.now(),
		nullable=True
	)

	def __init__(self, task, complete, user_id, created_at):
		self.task = task
		self.complete = complete
		self.user_id = user_id
		self.created_at = created_at
