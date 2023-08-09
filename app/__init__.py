from flask import Flask

from flask_restx import Api
from flask_migrate import Migrate

from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.models import User
from app.exts import db
from flask_marshmallow import Marshmallow

from app.resources.auth import auth_namespace
from app.resources.reset_password import reset_password_namespace
from app.resources.task import task_namespace

def create_app(config_class):
	app = Flask(__name__)
	# Configuration
	ma = Marshmallow(app)
	app.config.from_object(config_class)

	db.init_app(app)

	Migrate(app, db)

	JWTManager(app)
	CORS(app)

	api = Api(app, title='Authentication API', doc='/')
	api.add_namespace(auth_namespace, path='/api/auth')
	api.add_namespace(reset_password_namespace, path='/api/')
	api.add_namespace(task_namespace, path='/api/task')

	@app.shell_context_processor
	def make_shell_context():
		return { 'db': db, 'User': User }

	return app