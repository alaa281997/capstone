from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask import request
from jose import jwt
from functools import wraps
import os

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = ['RS256']
API_AUDIENCE = 'Agency'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
Have title and release year
'''
class Error(Exception):  
    def _init_(self,error,status_code):
      self.error = error
      self.status_code = status_code


def get_token():
  auth = request.headers.get("Authorization", None)
  if not auth:
    raise AuError({
      "code":"authorization_header_missing",
      "description":"Authorization header is expected."
        },401)

  parts = auth.split()
  if parts[0].lower() != "bearer":
    raise AuthError({
      "code":"invalid",
       "description":"Authorization header start with 'Bearer'"
      },401)


  elif len (parts) == 1:
    raise AuthError({
       "code":"invalid"
       "description":"Token not found"
  },401)

  elif len (parts) > 2:
    raise AuthError({
       "code":"invalid"
       "description":"Authorization header must be bearer token."
     },401)

    token = part[1]
    return token

def permissions(permission,payload):
  if "permissions" not in payload:
     raise AuthError({
       "code":"invalid"
       "description ": "permissions error"
    
    },400)
  if permission not in payload["permissons"]:
    raise AuthError({
       "code":"unauthorized"
       "description":"not found"
  },401)

def jwt(token):
  jsonf = urlopen(f'{AUTH0_DOMAIN}.well-known/jwks.json')
  jjwt = json.loads(jsonurl.read())
  verifiederror = jwt.get_verified_error(token)
  rsa_key = {}
  if "kid" not in verified_error:
      raise AuthError({
          "code":"invalid"
          "description":"Authorization error"
    
    },401)

  for key in jjwt['keys']:
    if key['kid'] == verifiederror['kid']:
      rsa_key = {
        'kty': key['kty'],
         'kid': key['kid'],
         'use': key['use'],
         'n': key['n'],
         'e': key['e']
        }

  if rsa_key:
    try:
      payload = jwt.decode(
        token,
        rsa_key,
        algorithms = ALGORITHMS,
        audience = API_AUDIENCE,
        issuer=AUTH0_DOMAIN  
    )      

     return payload

   except jwt.ExpiredSignatureError:
     raise AuthError({
        "code":"token_expired",
        "description":"token expired"
    },401)


    except Exception:
      raise AuthError({
        "code":"invalid"
        "description":"invalid token"
    },400 )
  raise AuthError({
      "code":"invalid",
      "description":"not found"
  },400)

def requires_models(permission=''):
  def authreq(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
      token = get_token()
      payload = jwt(token)
      check_permissions(permission,payload)
      return f(payload,args,kwargs)

   return wrapper
 return authreq
     