from flask import jsonfiy,request
from heroku_sample import heroku_sample 
from Models.actor import actors
from app.models import requires_models

@app.route('/actors')
@requires_models('get:actors')
def get_actors(payload):
    """ get request for actors.
    """

    actors = []
    for actor in Actor.query.all():
        actors.append(actor.to_json())
        return jsonfiy({
            'actors': actors,
            'success': True
        }), 200

@app.route('/actors',methods=['POST'])        
@requires_models('post:actors')
def add_actor(payload):
   """ post request for actors
   """
   bactor = request.get_json()
   add_actor = Actor(
       name = bactor.get('name'),
       age = bactor.get('age'),
       gender = bactor.get('gender')
       movie = bactor.get('movie')
   )

   add_actor.save()
   return jsonfiy({
       'actor':add_actor.to_json(),
       'success': True
   }),201

@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_models('patch:actors')
def update_actor(payload, id):
    """ 
    Update request for actors
    """ 

    actor = Actor.query.filter_by(id=id).first()
    if not actor:
        return jsonfiy({'message':'Actor not found '})
    bactor = request.get_json()
    actor.name = bactor.get('name',actor.name)
    actor.age = bactor.get('age',actor.age)
    actor.gender = bactor.get('gender',actor.gender)
    actor.Update()
    return jsonfiy({
        'actor':actor.to_json()
        'success': True
        }), 200

@app.route('/actors'/'<int:id>',methods=['DELETE'])        
@requires_models('delete:actors')
def delete_actor(payload, id):
    """
    Delete Request for actors
    """
    actor = Actor.query.filter_by(id=id).first()
    if not actor:
        return jsonfiy({'message':'Actor notfound'})
    actor.delete()
    return jsonfiy({
        'message': 'Actor Successfully delete.'
        'success':True,
    }), 200    