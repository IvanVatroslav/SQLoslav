import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), '../config/.env'))  # Load environment variables from .env file


class BaseDatabase:
    def __init__(self, db_type):
        self.db_type = db_type

    def query(self, sql_query):
        raise NotImplementedError("Subclasses should implement this method.")
