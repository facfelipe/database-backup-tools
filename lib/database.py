#!/usr/bin/python3
import pymysql

class Factory:

	def fromConfig(config):		
		return Database(host=config['host'], user = config['user'], password=config['password'], database=config['database'])

class Database(object):

	host = None
	user = None
	password = None
	database = None

	connection = None

	def __init__(self, **kwargs):

		for arg in ["host", "user", "password", "database"]:
			value = kwargs.pop(arg, None)
			setattr(self, arg, value)

	def connect(self):

		self.connection = pymysql.connect(
			host=self.host,
			user=self.user,
			password=self.password,
			cursorclass=pymysql.cursors.DictCursor
		)

	def execute(self, query, commit=True):

		self.connect()

		with self.connection:
			with self.connection.cursor() as cursor:
				cursor.execute(query)

				if(commit):
					self.connection.commit()

