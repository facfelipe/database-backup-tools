#!/usr/bin/python3
import argparse
from lib import utils, database, dumper

def dump(compressed = True):
	
	db = database.Factory.fromConfig(utils.loadConfig('DB_PRODUCTION'))

	filepath = utils.loadConfig('BACKUP')['path']

	return dumper.dump(db, filepath=filepath, compressed=compressed)

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('--skip-notification', help='skip notification on Slack')
	args = parser.parse_args()

	file = dump()

	if not args.skip_notification:
		utils.notify('BACKUP_NOTIFICATION')
	else:
		print("Backup finished. Dump file in: %s" % (file))