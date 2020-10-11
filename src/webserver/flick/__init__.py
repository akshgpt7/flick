import os
from flask import Flask

def create_app():

   app = Flask(__name__, instance_relative_config=True)

   @app.route('/')
   def flick():
      return 'Welcome to flick!'

   if __name__ == '__main__':
      app.run(debug=True)

   from . import db
   db.init_app(app)

   with app.app_context():
       from . import joints
       from . import order
       app.register_blueprint(joints.bp)
       app.register_blueprint(order.bp)
       app.add_url_rule('/', endpoint='index')

   return app
