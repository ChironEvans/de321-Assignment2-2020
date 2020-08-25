# Code by Chiron Evans
from pymongo import MongoClient, errors


class MongoCursor:

    def __init__(self):
        self.conn_str = 'mongodb://localhost:27017'
        self.client = MongoClient(self.conn_str, serverSelectionTimeoutMS=2000)
        self.db = self.client.jsparser

    async def add_entry(self, payload, name='default'):
        """Adds an entry to a MongoDB Database, Takes an arbitrary entry name & a payload.
        Payload must be a dictionary of information gathered from an analysed JS file"""
        if name.strip(' ') == '':
            name = 'default'
        if payload is not None:
            if self.connection():
                query = self.db.jparser.analysed.update_one({'name': name}, {'$set': {'data': payload}}, upsert=True)

                # Uncomment for debug
                # print(f'Modified: {query.modified_count}')
                # print(query, type(query))
                # print(query.raw_result)

                if query.raw_result['ok'] == 1.0:
                    return True
                else:
                    return False
        return False

    async def fetch_entry(self, name='default'):
        """Fetches a previously added entry from a MongoDB database using the name given by the user"""
        if self.connection():
            if not self.db.jparser.analysed.find_one({'name': name}):
                return False
            else:
                query = self.db.jparser.analysed.find_one({'name': name})
                return query
        else:
            return False

    async def delete_entry(self, name='default'):
        """Deleted an entry from the database, using the name given to the entry by the user"""
        if self.connection():
            if not self.db.jparser.analysed.find_one({'name': name}):
                return False
            else:
                query = self.db.jparser.analysed.delete_one({'name': name})
                return query
        else:
            return False

    # connection function code by Liam
    def connection(self):
        """Checks whether there's a valid connection to MongoDB database should not be called directly"""
        try:
            self.client.server_info()
        except errors.ServerSelectionTimeoutError:
            return False
        return True
