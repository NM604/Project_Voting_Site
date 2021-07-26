import os
from flask import Flask, render_template, flash
import psycopg2
import dj_database_url
from . import db

def create_app(test_config=None):
  app = Flask("votingsite")
  app.secret_key = 'very_secret_key'
  os.environ['DATABASE_URL'] = postgres://mlhdpdlvisnyjz:50f16d388f1aeae421cc52ca71201b1b274d1be7b5edbe6fa213a8560a983074@ec2-3-237-55-151.compute-1.amazonaws.com:5432/d72i87oqrosauq
  DATABASES = { 'default': dj_database_url.config() }
  DATABASE_URL = os.environ['DATABASE_URL']
  if test_config is not None:
    app.config.update(test_config)
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass
  
  from . import vote
  app.register_blueprint(vote.bp)
  
  from . import db
  db.init_app(app)
  
  return app
