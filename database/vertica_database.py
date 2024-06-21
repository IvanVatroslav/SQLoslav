import pandas as pd
import vertica_python
import os
import logging
from database.base_database import BaseDatabase


class VerticaDatabase(BaseDatabase):
    def __init__(self):
        super().__init__('vertica')
        self.conn_info = {
            'host': os.getenv('VERTICA_HOST'),
            'port': int(os.getenv('VERTICA_PORT')),
            'user': os.getenv('VERTICA_USER'),
            'password': os.getenv('VERTICA_PASSWORD'),
            'database': os.getenv('VERTICA_DATABASE'),
        }
        logging.info("Initializing VerticaDatabase")
        logging.info(f"Connection info: {self.conn_info}")

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
            return pd.DataFrame()
