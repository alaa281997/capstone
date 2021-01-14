from heroku_sample import heroku_sample
from heroku_sample.Models.movie import heroku_sample
from heroku_sample.models import requires_models

@app.route('/movies')
@requires_models('get:movies')
def get_movies(payload):
    """
    get request form movies
    """

movies = []
for movie in Movie.query.all():
    movie.append(movie.to_json())  
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
     
    bmovie = request.get_json()
    add_movie = Movie(
        title = bmovie.get('title'),
        date = bmovie.get('date')

    )
    
    add_movie.save()
    return jsonify({
        'movie':add_movie.to_json(),
         'success': True 
        }),201

@app.route('/movies',methods=['PATCH'])
@requires_models('Patch:movies')
   """
   update movie
   """

   movie = Movie.query.filter_by(id=id).first()
   if not movie:
       return jsonify({'message':'Movie not found'})
    bmovie = request.get_json()
    movie.title = bmovie.get('title',movie.title)
    movie.date = bmovie.get('date'),
    movie.update()
    return jsonify({
        'movie': movie.to_json(),
        'success':True
    }), 200

@app.route('/movies/<int:id>',methods=['DELETE']) 
@requires_models('delete:movies')
def del_movies(id):
    """
    del request for movie
    """
    movie = Movie.query.filter_by(id=id).first()
    if not movie:
        return jsonify({'message':'Movie not found'})
    movie.delete()
    return jsonify({
        'message': 'deleted'
        'success':True,
    }),200  
   
