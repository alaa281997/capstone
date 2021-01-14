import os
from flask import Flask, jsonify
from models import setup_db
from config import Config 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import actor, movie
from app.routes import index, actors, movies


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success":False,
        "error":401,
        "message":"unauthorized"
    }),401

@app.errorhandler(401)
def invalid(error):
    return jsonify({
        "success":False,
        "error":401,
        "message":"invalid"
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
        "message":"not allowed"
    }),405

@app.errorhandler(422)
def notable(error):
    return jsonify({
        "success":False,
        "error":422,
        "message":"Notable"
    }),422





