from flask import make_response, request, jsonify
from flask_restx import Resource, Namespace, fields

from flask_jwt_extended import create_access_token, decode_token
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError

from app.resources.errors import (
	UnauthorizedError,
	InternalServerError,
	EmailDoesnotExistsError,
	PasswordLengthError,
	BadTokenError,
	ExpiredTokenError
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app.exts import db
import datetime

reset_password_namespace = Namespace('reset', description='A namespace for reset password')

forgot_password_model = reset_password_namespace.model(
	'ForgotPassword', {
		'email': fields.String
	}
)

reset_password_model = reset_password_namespace.model(
	'ResetPassword', {
		'reset_token': fields.String,
		'password': fields.String
	}
)

reset_password_known_model = reset_password_namespace.model(
	'ResetPassword', {
		'old_password': fields.String,
		'new_password': fields.String,
		'new_password_again': fields.String
	}
)

@reset_password_namespace.route('/forgot-password')
class ForgotPasswordResource(Resource):
	@reset_password_namespace.expect(forgot_password_model)
	def post(self):
		try:
			body = request.get_json()
			user = User.query.filter_by(email=body.get('email')).first()
			if not user:
				raise EmailDoesnotExistsError

			expires = datetime.timedelta(hours=12)
			reset_token = create_access_token(str(user.id), expires_delta=expires)

			return make_response(jsonify({
				'reset_token': reset_token
			}), 201)

		except EmailDoesnotExistsError:
			raise EmailDoesnotExistsError

		except Exception as e:
			raise InternalServerError

@reset_password_namespace.route('/reset-password-known')
class ResetPasswordKnownResource(Resource):
	@reset_password_namespace.doc(security="jsonWebToken")
	@jwt_required()
	@reset_password_namespace.expect(reset_password_known_model)
	def post(self):
		# try:
		body = request.get_json()
		# if len(body.get('password')) < 6:
		# 	raise PasswordLengthError

		user_id = get_jwt_identity()
		user = User.query.filter_by(id=user_id).first()
		if not check_password_hash(user.password, body.get('old_password')):
			raise UnauthorizedError
		if body.get('new_password') != body.get('new_password_again'):
			return make_response(jsonify({
			'message': 'Your passwords dont match'
		}), 403)
		hashed_password = generate_password_hash(body.get('new_password'))
		user.password = hashed_password
		db.session.commit()

		return make_response(jsonify({
			'message': 'Your password has been changed.'
		}), 201)

		# except PasswordLengthError:
		# 	raise PasswordLengthError

		# except ExpiredSignatureError:
		# 	raise ExpiredTokenError

		# except (DecodeError, InvalidTokenError):
		# 	raise BadTokenError

		# except Exception as e:
		# 	raise InternalServerError


@reset_password_namespace.route('/reset-password')
class ResetPasswordResource(Resource):
	@reset_password_namespace.expect(reset_password_model)
	def post(self):
		try:
			body = request.get_json()
			# if len(body.get('password')) < 6:
			# 	raise PasswordLengthError

			user_id = decode_token(body.get('reset_token'))['sub']
			user = User.query.filter_by(id=user_id).first()

			hashed_password = generate_password_hash(body.get('password'))
			user.password = hashed_password
			db.session.commit()

			return make_response(jsonify({
				'message': 'Your password has been changed.'
			}), 201)

		except PasswordLengthError:
			raise PasswordLengthError

		except ExpiredSignatureError:
			raise ExpiredTokenError

		except (DecodeError, InvalidTokenError):
			raise BadTokenError

		except Exception as e:
			raise InternalServerError