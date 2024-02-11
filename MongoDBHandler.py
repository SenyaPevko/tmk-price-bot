import logging
from pymongo import MongoClient


class MongoDBHandler(logging.Handler):
    def __init__(self, db_name, collection_name, host='localhost', port=27017):
        super().__init__()
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def emit(self, record):
        log_entry = {
            'timestamp': self.format(record),
            'level': record.levelname,
            'message': record.msg,
            'logger_name': record.name
        }
        self.collection.insert_one(log_entry)
