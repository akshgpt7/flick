import os
from flask import Flask

def create_app():

   # create and configure the app
   app = Flask(__name__, instance_relative_config=True)

   app.config.from_mapping(
      SECRET_KEY='dev',
      DATABASE='../../../data/database.db'
   )

   app.config.from_pyfile('config.py', silent=True)

   @app.route('/')
   def hello_world():
      return 'Hello World'

   if __name__ == '__main__':
      app.run(debug=True)

   from . import db
   db.init_app(app)

   from . import joints
   app.register_blueprint(joints.bp)
   app.add_url_rule('/', endpoint='index')

   return app
