import pandas as pd
import vertica_python
import os
import logging
from database.base_database import BaseDatabase


class VerticaDatabase(BaseDatabase):
    def __init__(self):
        super().__init__('vertica')
        # Set default values for connection parameters
        default_port = 5433  # Default Vertica port
        
        # Get environment variables with defaults
        vertica_host = os.getenv('VERTICA_HOST')
        vertica_port = os.getenv('VERTICA_PORT', str(default_port))
        vertica_user = os.getenv('VERTICA_USER')
        vertica_password = os.getenv('VERTICA_PASSWORD')
        vertica_database = os.getenv('VERTICA_DATABASE')
        
        # Log warning if any required environment variables are missing
        if not all([vertica_host, vertica_user, vertica_password, vertica_database]):
            logging.warning("Some Vertica connection parameters are missing. Connection may fail.")
            if not vertica_host:
                logging.warning("VERTICA_HOST environment variable is not set")
            if not vertica_user:
                logging.warning("VERTICA_USER environment variable is not set")
            if not vertica_password:
                logging.warning("VERTICA_PASSWORD environment variable is not set")
            if not vertica_database:
                logging.warning("VERTICA_DATABASE environment variable is not set")
        
        self.conn_info = {
            'host': vertica_host,
            'port': int(vertica_port),  # Convert to int with default already applied
            'user': vertica_user,
            'password': vertica_password,
            'database': vertica_database,
        }
        logging.info("Initializing VerticaDatabase")
        # Log connection info with password masked
        safe_conn_info = self.conn_info.copy()
        if 'password' in safe_conn_info:
            safe_conn_info['password'] = '********'
        logging.info(f"Connection info: {safe_conn_info}")

    def query(self, sql_query: str):
        logging.info(f"Database query: {sql_query}")
        try:
            with vertica_python.connect(**self.conn_info) as connection:
                with connection.cursor() as cur:
                    cur.execute(sql_query)
                    df = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
                    logging.info(f"Query returned {len(df)} rows.")
            return df
        except vertica_python.Error as e:
            logging.error(f"An error occurred: {e}")
            raise Exception(f"Vertica database error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error connecting to Vertica: {e}")
            raise Exception(f"Failed to connect to Vertica database: {e}")
