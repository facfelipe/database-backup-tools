#!/usr/bin/python3
import backup
from lib import utils, database
import pymysql.cursors
import os, glob, sys

delete_file_after_clone = False

def getLatestBackupFileOrDump():

	global delete_file_after_clone

	dir = utils.loadConfig('BACKUP')['path']

	files = glob.glob(dir + "/*.gz")

	if not files:
		delete_file_after_clone = True
		return backup.dump(False)

	file = max(files, key=os.path.getctime)

	os.system('gzip -d -k %s' % (file))

	sqlfile = file.rsplit( ".", 1 )[0]

	return sqlfile

def clone():

	file = getLatestBackupFileOrDump()

	db = database.Factory.fromConfig(utils.loadConfig('DB_STAGING'))

	db.execute('''DROP DATABASE IF EXISTS %s''' % (db.database))

	db.execute('''CREATE DATABASE %s''' % (db.database))

	db.execute('''SET GLOBAL FOREIGN_KEY_CHECKS=0;''')

	cmd = "mysql -h %s -u %s -p%s %s < %s" % (db.host, db.user, db.password, db.database, file)

	os.system(cmd)

	db.execute('''SET GLOBAL FOREIGN_KEY_CHECKS=1;''')

	if(delete_file_after_clone):
		os.system('rm ' + file)


if __name__ == "__main__":

	clone()

	utils.notify('CLONE_NOTIFICATION')