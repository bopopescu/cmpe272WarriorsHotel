import sys
import pymongo
import dns # required for connecting with SRV
from pymongo.errors import ConnectionFailure

# mongodbSvr1 = "mongodb-2745-0.cloudclusters.net:10005/admin -u warriors -p warriors --authenticationDatabase "admin""

class AppDB():
    def __init__(self):
        self.client= mongomock.MongoClient()
        self.db = self.client["db.DB"]


    def list_calendar(db):
        collection=db['DATABASE.calendar']
        return (collection)

    def get_one_calendar(db):
        calendar_listing_date = dict()
        calendar=db['DATABASE.calendar']
        q = calendar.find({'date' : date})
        if q:
            output = q
        else:
            output = 'No results found'
        return (q)


