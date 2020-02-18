import datetime


from peewee import *


from flask_login import UserMixin


DATABASE = SqliteDatabase('goals.sqlite')

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
	

