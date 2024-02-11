import logging
import os

from dotenv import load_dotenv

from MongoDBHandler import MongoDBHandler


class Logger(logging.Logger):

    def __init__(self, name, level=logging.INFO):
        super().__init__(name, level)
        load_dotenv()
        self.db_name = os.getenv("bot_db_name")
        self.db_host = os.getenv("db_host")
        self.db_port = os.getenv("db_port")
        self.db_collection_name = os.getenv("logs_collection_name")
        self.db_handler = MongoDBHandler(self.db_name, self.db_collection_name, self.db_host, int(self.db_port))
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(self.formatter)

        self.addHandler(self.db_handler)
        self.addHandler(ch)
