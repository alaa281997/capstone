import os 
from flask import Flask, jsonify     
from models import setup_db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Actor, Movie , setup_db


@app.route('/')
def index():
    """ 
    get requests
    """
    return jsonify({
       'message': 'Capstone',
        'success': True
    }))

@app.route('/actors')
@requires_models('get:actors')
def get_actors(payload)
  """get actors route
  """"
  actors = Actor.query.all()
   return jsonify({
       'actors':actors,
       'success':True
       }), 200
@app..route('/actors',methods=['POST'])
@requires_models('post:actors')
def post_actor(payload)
    """
      post actors route
    """
    postactor = request.get_json()
    name = postactor.get('name')
    age = postactor.get('age')
    gender = postactor.get('gender')

    actor = Actor(name = name , age = age , gender = gender)

    if name is None or age is None or gender is None:
        abort (400)

    try:
        actor.insert()
        return jsonify({
            'success' = True,
             'actor' = actors
        }), 201 

    except Exception:
        abort (500)
@app.route('/actors/<int:id>',methods=['PATCH'])
@requires_models('patch:actors')
    """
    update actor
    """
    
    upactor = request.get_json()
    name = upactor.get('name')
    age = upactor.get('age')
    gender = upactor.get('gender')

    actor = Actor.query.get(id)

    if actor is None:
        abort(404)
    if name is None or age is None or gender is None:
        abort (400)
    
    actor.name = name
    actor.age = age
    actor.gender = gender

    try:
        actor.update()
        return jsonify({
            'actor':actor,
            'success':True
        }),200 

    except Exception:
        abort(500)

@app.route('/actors/,<int:id>',methods=['DELETE'])
@requires_models('delete:actors')
def delete_actor(payload):
    """
    Delete Actor
    """
    actor = Actor.query.get(id)

    if actor in None:
        abort(404)
    try:
        actor.delete()
        return jsonify({
            'message' :'Successfully deleted',
             'success' :True
        })    

    except Exception:
        db.session.rollback()
        abort (500)


@app.route('/movies')
@requires_models('get:movies')
def get_movies(payload):
    """
    get movies route
    """
    movies = Movie.query.all()
    
    return jsonfiy({
        'movies': movies,
        'success' : True
}), 200

@app.route('/movies', methods=['POST'])
@requires_models('post:moives')
def add_movie():
    """
    post request for movies 
    """
    requestmov = request.get_json()
    title = requestmov.get('title')
    date = requestmov.get('date')
   
    if title is None or date is None:
        abort(400)

    movie = Movie(title=title, date = date)

    try:
        movie.insert()
        return jsonify({
            'success':True,
            'movie':movie.format()
        }),201
    except Exception:
        abort(500)


@app.route('/movies/<int:id>',methods=['PATCH'])
@requires_models('Patch:movies')
   """
   update movie
   """

    upmovie = request.get_json()
    title = upmovie.get('title')
    date = upmovie.get('date')

    movie = Movie.query.get(id)
    if movie is None:
        abort(404)
    if title is None or date is None:
        abort(400)

    movie.title = title
    movie.date = date
    
    try:
        movie.update()
        return jsonify({
            'movie': movie.format(),
            'success':True
    }), 200

    except Exception:
        abort(500)

@app.route('/movies/<int:id>',methods=['DELETE']) 
@requires_models('delete:movies')
def del_movies(id):
    """
    del request for movie
    """
    movie = Movie.query.get(id)

    if movie is None:
        abort(404)
    try:
        movie.delete()
        return jsonify({
            'message': 'deleted'
            'success':True,
    })
    except Exception:
        db.session.rollback()
        abort(500)  
   

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success":False,
        "error":401,
        "message":"unauthorized"
    }),401


@app.errorhandler(404)
def notfound(error):
    return jsonify({
        "success":False,
        "error":404,
        "message":"not found"
    }),404

@app.errorhandler(405)
def notallowed(error):
    return jsonify({
        "success":False,
        "error":405,
        "message":"Method not allowed"
    }),405

@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        "success":False,
        "error":422,
        "message":"Unprocessable_entity"
    }),422

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success":False,
        "error":500,
        "message":"internal server error"
    })




