# {
#     "99popularity": 83.0,
#     "director": "Victor Fleming",
#     "genre": [
#       "Adventure",
#       " Family",
#       " Fantasy",
#       " Musical"
#     ],
#     "imdb_score": 8.3,
#     "name": "The Wizard of Oz"
#   },

from flask_bcrypt import generate_password_hash, check_password_hash

from .db import db

class Movie(db.Document):
    name = db.StringField(required=True)
    director = db.StringField(required=True)
    genres = db.ListField(db.StringField(), required=True)
    imdb_score = db.FloatField(required=True)
    popularity99 = db.FloatField(required = True)

class User(db.Document):
    email = db.EmailField(required=True, unique = True)
    password = db.StringField(required=True, min_length=6)
    is_admin = db.BooleanField(default=False)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')
    
    def check_password(self,password):
        return check_password_hash(self.password, password)