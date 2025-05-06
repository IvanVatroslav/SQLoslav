import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod

# Try to load environment variables from different possible locations
# but don't fail if no .env file is found (as in production environments like Render)
try:
    # First try the root directory
    if os.path.exists(os.path.join(os.getcwd(), '.env')):
        load_dotenv(os.path.join(os.getcwd(), '.env'))
    # Then try config directory
    elif os.path.exists(os.path.join(os.getcwd(), 'config', '.env')):
        load_dotenv(os.path.join(os.getcwd(), 'config', '.env'))
    # Finally try relative to this file
    elif os.path.exists(os.path.join(os.path.dirname(__file__), '../.env')):
        load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
    # No need to fail if .env is not found - in production systems like Render,
    # environment variables are set through the dashboard
except Exception as e:
    print(f"Note: Could not load .env file, but this is fine in production: {e}")


class BaseDatabase:
    def __init__(self, db_type):
        self.db_type = db_type

    def query(self, sql_query):
        raise NotImplementedError("Subclasses should implement this method.")
