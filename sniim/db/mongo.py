import os
from urllib.parse import quote_plus
from pymongo import MongoClient


class Mongoclient:
    def __init__(self, *args, db_collection=None):
        self.host = os.environ.get('MONGO_HOST', '0.0.0.0')
        self.port = os.environ.get('MONGO_PORT', '27017')
        if os.environ.get('CONNECT_WITH_USER', 'False') == 'True':
            self.user = os.environ.get('MONGO_USER', 'central')
            self.password = os.environ.get('MONGO_PASSWORD', 'central')

        self.client = MongoClient(self._connection_string)
        self.db_name = os.environ.get('MONGO_DATABASE', 'central')
        self.db_collection = db_collection

        self.db = self.client[self.db_name]
        self.collection = self.db[self.db_collection]

    @property
    def _connection_string(self):
        if os.environ.get('CONNECT_WITH_USER', 'False') == 'True':
            return "mongodb://{0}:{1}@{2}:{3}".format(self.user, self.password, self.host, self.port)
        else:
            return "mongodb://{0}:{1}".format(self.host, self.port)

    def insert_one(self, document):
        inserted = self.collection.insert_one(document)
        return True if getattr(inserted, 'inserted_id') else False
