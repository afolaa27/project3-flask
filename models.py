import datetime
import os

from peewee import *


from flask_login import UserMixin
from playhouse.db_url import connect

#DATABASE = SqliteDatabase('goals.sqlite')

if 'ON_HEROKU' in os.environ: # later we will manually add this env var 
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this 
                                                     # env var for you 
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
else:
  DATABASE = SqliteDatabase('goals.sqlite')

  # OPTIONALLY: instead of the above line, here's how you could have your 
  # local app use PSQL instead of SQLite:

  # DATABASE = PostgresqlDatabase('dog_demo', user='reuben')  

  # the first argument is the database name -- YOU MUST MANUALLY CREATE 
  # IT IN YOUR psql TERMINAL
  # the second argument is your Unix/Linux username on your computer



  
class User(UserMixin,Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField()

	class Meta:
		database = DATABASE


class Goal(Model):
	title = CharField()
	description = CharField()
	created_date = DateTimeField(default=datetime.datetime.now)
	deadline = DateTimeField()
	before_deadline = IntegerField()
	owner = ForeignKeyField(User, backref='goals')

	class Meta:
		database =DATABASE

def initialize():
	DATABASE.connect()


	DATABASE.create_tables([User, Goal], safe=True)
	print('connected to the DB and tables created')


	DATABASE.close()
	

