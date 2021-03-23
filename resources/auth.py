from flask import request, Response
from database.models import User
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, \
    NotUniqueError, DoesNotExist, ValidationError, \
    InvalidQueryError
from resources.errors import SchemaValidationError,  \
    InternalServerError, EmailAlreadyExistsError, UnauthorizedError


class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User(**body)
            user.hash_password()
            user.save()
            id = user.id
            return {'id':str(id)},200
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception as e:
            raise InternalServerError

class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            print(user.is_admin)
            authorized = user.check_password(body.get('password'))
            print(user)
            print(authorized)
            if not authorized:
                raise UnauthorizedError
            return {'success':'true','is_admin':user.is_admin}, 200
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception as e:
            raise InternalServerError
        