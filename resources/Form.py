from wtforms import Form, TextField, StringField, FormField, TextAreaField, PasswordField, validators, FloatField, FieldList
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class RegisterForm(Form):
    email = EmailField('Email Address', validators=[DataRequired(), Email()])    
    password = PasswordField('Password', [
        DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

class GenreForm(Form):
    name = StringField('Genre', [validators.Length(min=5, max=20)])

class MovieForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    director = StringField('Director', [validators.Length(min=1, max=50)])
    genres = TextField('Genres', [validators.Length(min=3, max=50)])
    imdb_score = FloatField('IMDB-SCORE', [validators.NumberRange(min=1, max=10)])
    popularity99 = FloatField('Popularity99', [validators.NumberRange(min=1, max=100)])

