#!/usr/bin/python3
import os
import time
from lib import database

def dump(Database, filepath="./dumps", compressed = True):

    filestamp = time.strftime('%Y-%m-%d-%I:%M')
    filename = Database.database+"_"+filestamp
    ext = '.sql.gz' if compressed else '.sql'
    file = filepath + "/" + filename + ext

    cmd = "mysqldump -h %s -u %s -p%s --compact --column-statistics=0 --no-tablespaces %s " + ("| gzip -c > %s" if compressed else "> %s")
    
    os.system(cmd % (Database.host, Database.user, Database.password, Database.database, file))
    
    return file
