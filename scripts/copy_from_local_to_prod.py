from pymongo import MongoClient
from database import FLASK_MONGODB_SETTINGS

import sys

# CONNECT TO PROD
master_db = MongoClient(FLASK_MONGODB_SETTINGS['host'])['recipes']
# CONNECT TO LOCAL
local_db = MongoClient("mongodb://localhost:27017")['recipes']

input("START COPYING? [enter]")

count = 0

for doc in local_db.get_collection('recipe').find():
    master_db.get_collection('recipe').insert_one(doc)
    print('.', end='')
    sys.stdout.flush()
    count += 1

print(f'COPIED {count} DOCS!')
print('END!')
