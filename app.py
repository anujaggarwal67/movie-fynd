from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from flask_bcrypt import Bcrypt
from database.db import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from resources.errors import errors
from resources.Form import RegisterForm, MovieForm
import requests
from functools import wraps
from database.models import Movie
import json
from os import getcwd, path, getenv

# Reading configurations
configfile = path.join(getcwd(), 'config', 'config.json')
print('Reading configuration',configfile)
config = json.load(open(configfile))
# print(environ)
env = getenv("env")
print('current env: ', env)

# This url will be populated from the configuration for different test and production environments
apiurl = config[env]['url']
app = Flask(__name__)
api = Api(app, errors = errors)

app.config['MONGODB_SETTINGS'] = {
    'host': getenv("mongodb_host")
}

# decorator to check if a user is logged in or not
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


# decorator to check if user is admin or not
def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_admin' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            session.clear()
            return redirect(url_for('login'))
    return wrap


# index route to navigate to the home page
@app.route('/')
def index():
    return render_template('home.html')


# register route to register the user 
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        json = {}
        json['email'] = email
        json['password'] = password
        r = requests.post(url = apiurl+"/api/signup", json=json)
        print('status code is ', r.status_code)
        if r.status_code==200:
            flash('you are now registered','success')
            return redirect(url_for('login'))
        elif r.status_code == 500:
            flash('Email Already Exists','error')
            return render_template('register.html', form = form)
        
    return render_template('register.html', form = form)

# login route to logged in the user
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        #get form fields
        email = request.form['email']
        password = request.form['password']
        json = {}
        json['email'] = email
        json['password'] = password
        r = requests.post(url = apiurl+"/api/login", json=json)
        if r.status_code == 200:
            session['logged_in'] = True
            session['username'] = email
            session['is_admin'] = r.json()['is_admin']
            flash('you are logged in','success')
            return redirect(url_for('dashboard'))
        else:
            flash('you are not registered or your username and password is wrong','error')
            return render_template('login.html')
    return render_template('login.html')

# dashboard route to show all the movies to the user and admin
@app.route('/dashboard',methods=['GET','POST'])
@is_logged_in
def dashboard():
    
    if request.method=="POST":
        name = request.form['moviename']
        searchstring = name.split(" ")
        genre = request.form['genre']
        result = []
        if genre.lower() == 'all':
            if name=="":
                r = requests.get('http://localhost:5000/api/movies')
                result = r.json()
            else:
                result = Movie.objects(name=name).to_json()
                result = json.loads(result)
        else:
            print(genre.capitalize())
            genre = genre.capitalize()
            if name=="":

                result = Movie.objects(genres__in=[genre]).to_json()
            else:
                result = Movie.objects(name=name, genres__in=[genre]).to_json()
                print(result)
            result = json.loads(result)
            
        return render_template('dashboard.html',movies=result)
    r = requests.get('http://localhost:5000/api/movies')
    if (r.json()):
        return render_template('dashboard.html', movies=r.json())
    else:
        msg = 'No articles found'
        return render_template('dashboard.html', msg=msg)

# logout route to log out the user 
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('you are now logged out', 'success')
    return redirect(url_for('login'))


# add_movie route to add a movie if user is admin
@app.route('/add_movie', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def add_movie():
    form = MovieForm(request.form)
    if request.method=='POST' and form.validate():
        name = form.name.data
        director = form.director.data
        genres = form.genres.data.split(',')
        imdb_score = form.imdb_score.data
        popularity99 = form.popularity99.data
        json = {}
        json["name"] = name
        json["director"] = director
        json["genres"] = genres
        json["imdb_score"] = imdb_score
        json["popularity99"] = popularity99
        print(json)
        r = requests.post(url="http://localhost:5000/api/movies", json=json)
        if r.status_code==200:
            flash('Movie has been added succesfully', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('There is error in creating ,please give correct inpput','error')
            return render_template('add_movie.html', form=form)
    return render_template('add_movie.html', form=form)


# edit_movie route to update the movie if the user is admin
@app.route('/edit_movie/<id>', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def edit_movie(id):
    r = requests.get(url='http://localhost:5000/api/movies/'+id)
    form = MovieForm(request.form)
    form.name.data = r.json()['name']
    form.director.data = r.json()['director']
    form.genres.data = ','.join(r.json() ['genres'])
    form.imdb_score.data = r.json()['imdb_score']
    form.popularity99.data = r.json()['popularity99']


    if request.method=='POST' and form.validate():
        name = request.form['name']
        director = request.form['director']
        genres = request.form['genres'].split(',')
        imdb_score = request.form['imdb_score']
        popularity99 = request.form['popularity99']
        json = {}
        json["name"] = name
        json["director"] = director
        json["genres"] = genres
        json["imdb_score"] = imdb_score
        json["popularity99"] = popularity99
        print(json)
        r = requests.put(url="http://localhost:5000/api/movies/"+id, json=json)
        if r.status_code==200:
            flash('Movie updated', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('There is error in updating ,please give correct inpput','error')
            return render_template('edit_movie.html', form=form)
    return render_template('edit_movie.html', form=form)


# delete route to delete the movie if the user is admin
@app.route('/delete_movie/<id>',methods=['POST'])
@is_logged_in
@is_admin
def delete_movie(id):
    r = requests.delete('http://localhost:5000/api/movies/'+id)
    if r.status_code==200:
        flash('movie deleted successfully','success')
        
    else:
        flash('there is something wrong','error')
    return redirect(url_for('dashboard'))

# to initiliaze the db for the app
initialize_db(app)

# to initialize the routes for the apis
initialize_routes(api)

# to provide a simple interface for overriding Werkzeug's built-in password hashing utilities.
bcrypt = Bcrypt(app)

# secret key of the app
app.secret_key = 'secret123'

# to test the changes
app.run()