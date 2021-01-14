from flask import jsonify
from heroku_sample import heroku_sample

@app.route('/')
def index():
    """ 
    get requests
    """
    return jsonify({
       'message': 'Capstone',
        'success': True
    })