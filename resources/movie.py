from flask import Blueprint, Response, request
from database.models import Movie
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, \
    NotUniqueError, DoesNotExist, ValidationError, \
    InvalidQueryError
from resources.errors import SchemaValidationError, MovieAlreadyExistsError, \
    InternalServerError, UpdatingMovieError, DeletingMovieError, \
    MovieNotExistsError

movies = Blueprint('movies',__name__)

class MoviesApi(Resource):
    def __init__(self):
        Movie.create_index( [('name', 1), ('director', 1)], unique=True )


    def get(self):
        movies = Movie.objects().to_json()
        return Response(movies, mimetype='application/json', status = 200)


    def post(self):
        try:
            body = request.get_json()
            movie = Movie(**body).save()
            id = movie.id
            return {'id':str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise MovieAlreadyExistsError
        except Exception as e:
            raise InternalServerError

class MovieApi(Resource):
    def __init__(self):
        Movie.create_index( [('name', 1), ('director', 1)], unique=True )
        
    def put(self, id):
        try:
            body = request.get_json()
            Movie.objects.get(id=id).update(**body)
            return '',200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingMovieError
        except Exception:
            raise InternalServerError
    
    def delete(self, id):
        try:
            Movie.objects.get(id=id).delete()
            return '',200
        except DoesNotExist:
            raise DeletingMovieError
        except Exception:
            raise InternalServerError


    def get(self, id):
        try:
            movies = Movie.objects.get(id=id).to_json()
            return Response(movies, mimetype='application/json', status = 200)
        except DoesNotExist:
            raise InternalServerError

