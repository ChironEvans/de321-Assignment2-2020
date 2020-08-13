import pymongo


class MongoCursor:

    def __init__(self):
        self.conn_str = 'mongodb://localhost:27017'
        self.client = pymongo.MongoClient(self.conn_str)
        self.db = self.client.jsparser

    def add_entry(self, name, payload):
        query = self.db.jparser.analysed.update_one(payload, upsert=True)

        if query.modified_count > 0:
            return True
        else:
            return False

    def fetch_entry(self, name):
        if not self.db.jparser.analysed.find_one({'name': name}):
            return False
        else:
            query = self.db.jparser.analysed.find_one({'name': name})
            return query

    def delete_entry(self, name):
        if not self.db.jparser.analysed.find_one({'name': name}):
            return False
        else:
            query = self.db.jparser.analysed.delete_one({'name': name})
            return query
