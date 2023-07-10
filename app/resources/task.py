from flask import make_response, request, jsonify
from flask_restx import Resource, Namespace, fields

from flask_jwt_extended import jwt_required, get_jwt_identity
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError

from app.resources.errors import InternalServerError, BadTokenError, ExpiredTokenError

from app.models import Task
from app.exts import db
import datetime

authorizations = {
    'Basic Auth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    },
}
task_namespace = Namespace('task', security='Basic Auth', authorizations=authorizations, description='A namespace for tasks')

task_creation_model = task_namespace.model(
	'TaskCreation', {
		'task': fields.String,
        'complete': fields.Boolean
	}
)

task_deletion_model = task_namespace.model(
	'TaskCreation', {
		'task_id': fields.Integer,
	}
)

task_update_model = task_namespace.model(
	'TaskCreation', {
		'task_id': fields.Integer,
        'task': fields.String,
	    'complete': fields.Boolean
	}
)

@task_namespace.route('/')
class TaskGetResource(Resource):
    @jwt_required(refresh=True)
    def get(self):
        try:
            user_id = get_jwt_identity()
            return Task.query.filter_by(
                user_id=user_id
            )
        except ExpiredSignatureError:
            raise ExpiredTokenError
        except (DecodeError, InvalidTokenError):
            raise BadTokenError
        except Exception:
            raise InternalServerError


@task_namespace.route('/create')
class TaskCreateResource(Resource):
    @jwt_required(refresh=True)
    @task_namespace.expect(task_creation_model)
    def post(self):
        try:
            body = request.get_json()
            complete = body.get('complete')
            user_id = get_jwt_identity()
            task_str = body.get('task')
            db.session.add(
                Task(
                    task=task_str,
                    user_id=user_id,
                    complete=complete,
                    created_at=datetime.date.today()
                )
            )
            db.session.commit()
            return make_response(jsonify({
				'message': 'Your task has been created.'
			}), 201)
        except ExpiredSignatureError:
            raise ExpiredTokenError
        except (DecodeError, InvalidTokenError):
            raise BadTokenError
        except Exception:
            raise InternalServerError

@task_namespace.route('/delete')
class TaskDeleteResource(Resource):
    @jwt_required(refresh=True)
    @task_namespace.expect(task_deletion_model)
    def post(self):
        try:
            body = request.get_json()
            task_id = body.get('task_id')
            user_id = get_jwt_identity()
            Task.query.filter_by(
                id=task_id,
                user_id=user_id
            ).delete()
            db.session.commit()
            return make_response(jsonify({
				'message': 'Your task has been deleted.'
			}), 200)
        except ExpiredSignatureError:
            raise ExpiredTokenError
        except (DecodeError, InvalidTokenError):
            raise BadTokenError
        except Exception:
            raise InternalServerError

@task_namespace.route('/update')
class TaskUpdateResource(Resource):
    @jwt_required(refresh=True)
    @task_namespace.expect(task_update_model)
    def post(self):
        try:
            body = request.get_json()
            task_id = body.get('task_id')
            user_id = get_jwt_identity()
            complete = body.get('complete', None)
            task_str = body.get('task', None)
            task = Task.query.filter_by(
                id=task_id,
                user_id=user_id
            ).first()
            if task_str:
                task.task = task_str
            if complete:
                task.complete = complete
            db.session.commit()
            return make_response(jsonify({
				'message': 'Your task has been updated.'
			}), 200)
        except ExpiredSignatureError:
            raise ExpiredTokenError
        except (DecodeError, InvalidTokenError):
            raise BadTokenError
        except Exception:
            raise InternalServerError