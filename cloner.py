#!/usr/bin/python3
import backup
from lib import utils, database
import pymysql.cursors
import os

if __name__ == "__main__":

	file = backup.dump(False)

	db = database.Factory.fromConfig(utils.loadConfig('DB_STAGING'))

	db.execute('''DROP DATABASE IF EXISTS %s''' % (db.database))

	db.execute('''CREATE DATABASE %s''' % (db.database))

	cmd = "mysql -h %s -u %s -p%s %s < %s" % (db.host, db.user, db.password, db.database, file)

	os.system(cmd)

	utils.notify('CLONE_NOTIFICATION')