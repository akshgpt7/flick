import os
from flask import Flask

def create_app():

   app = Flask(__name__, instance_relative_config=True)

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
