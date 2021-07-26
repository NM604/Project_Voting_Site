import os
from flask import Flask, render_template, flash
import psycopg2
from . import db

def create_app(test_config=None):
  app = Flask("votingsite")
  app.secret_key = 'very_secret_key'
  app.config.from_mapping(DATABASE="DATABASE_URL")
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
