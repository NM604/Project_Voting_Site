import os
from flask import Flask, render_template
import psycopg2
from . import db

def create_app(test_config=None):
  app = Flask("votingsite")
  app.config.from_mapping(DATABASE="votingsite")
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
