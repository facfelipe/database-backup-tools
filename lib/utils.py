import configparser
import os

def loadConfig(key = False):
	
	config = configparser.ConfigParser()	
	config.read('conf.ini')

	return config if False == key else config[key]

def notify(key):

	config = loadConfig(key)

	cmd = 'curl -X POST --data-urlencode "payload={\\"text\\": \\"%s\\"}" %s' % (config['message'], config['slack_url'])
	
	os.system(cmd)