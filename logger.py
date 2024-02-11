import logging
import os

from dotenv import load_dotenv

from MongoDBHandler import MongoDBHandler


class Logger(logging.Logger):

    def __init__(self, name, level=logging.INFO):
        super().__init__(name, level)
        load_dotenv()

        # Initializing db handler
        self.db_handler = None
        self.init_bd_handler()

        # Creating and adding console handler
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(self.formatter)
        self.addHandler(ch)

        # Adding bd handler
        self.addHandler(self.db_handler)

    def init_bd_handler(self):
        db_name = os.getenv("bot_db_name")
        db_host = os.getenv("db_host")
        db_port = os.getenv("db_port")
        db_collection_name = os.getenv("logs_collection_name")
        self.db_handler = MongoDBHandler(db_name, db_collection_name, db_host, int(db_port))
