# Code by Chiron Evans
import pymongo


class MongoCursor:

    def __init__(self):
        self.conn_str = 'mongodb://localhost:27017'
        self.client = pymongo.MongoClient(self.conn_str)
        self.db = self.client.jsparser

    def add_entry(self, name, payload):
        """Adds an entry to a MongoDB Database, Takes an arbitrary entry name & a payload.
        Payload must be a dictionary of information gathered from an analysed JS file"""
        query = self.db.jparser.analysed.update_one({'name': name}, {'data': payload}, upsert=True)

        if query.modified_count > 0:
            return True
        else:
            return False

    def fetch_entry(self, name):
        """Fetches a previously added entry from a MongoDB database using the name given by the user"""
        if not self.db.jparser.analysed.find_one({'name': name}):
            return False
        else:
            query = self.db.jparser.analysed.find_one({'name': name})
            return query

    def delete_entry(self, name):
        """Deleted an entry from the database, using the name given to the entry by the user"""
        if not self.db.jparser.analysed.find_one({'name': name}):
            return False
        else:
            query = self.db.jparser.analysed.delete_one({'name': name})
            return query
