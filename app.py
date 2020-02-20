import os
from flask import Flask, jsonify, g 

from flask_cors import CORS

from flask_login import LoginManager

from resources.users import users
from resources.goals import goals

import models

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = "hjabjbsdhbafwhgbds"

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoNotExist:
		return None

@login_manager.unauthorized_handler
def unauthorized():
	return jsonify(
		data={
		'Error' : 'User not logged in'
		},
		message= 'You have to be logged in',
		status = 401
		),401


CORS(goals, origins=['http://localhost:3000','https://goals-app-react.herokuapp.com'],supports_credentials=True)
CORS(users, origins=['http://localhost:3000','https://goals-app-react.herokuapp.com'], supports_credentials=True)


app.register_blueprint(goals, url_prefix='/api/v1/goals')
app.register_blueprint(users, url_prefix='/api/v1/users')


@app.before_request
def before_request():
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	g.db.close()
	return response


if 'ON_HEROKU' in os.environ: 
  print('\non heroku!')
  models.initialize()

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT) 




