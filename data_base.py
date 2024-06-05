import pandas as pd
from sqlalchemy import create_engine
import vertica_python
import os
from dotenv import load_dotenv
import logging

load_dotenv()  # Load environment variables from .env file

class Database:
    ORACLE_CONFIG = {
        'SINONIMI': {
            'service_name': 'ugvirga.ugbb.net',
            'user': 'ugvirga_stage_user',
            'password': 'pZYhZ6hY'  # replace with actual password
        },
        'SHOPSTER': {
            'service_name': 'se2prod.ugbb.net',
            'user': 'shopster',
            'password': 'shop5terPsw1706'  # replace with actual password
        },
        'VIRGA_TEST': {
            'service_name': 'ugvirgatest.ugbb.net',
            'user': 'infapc',
            'password': 'sSwyGM9d'  # replace with actual password
        },
        'VIRGA': {
            'service_name': 'ugvirga.ugbb.net',
            'user': 'infapc',
            'password': 'P6DsQLeD'  # replace with actual password
        }
    }

    def __init__(self, db_name):
        db_name_upper = db_name.upper()
        if db_name_upper in self.ORACLE_CONFIG:
            config = self.ORACLE_CONFIG[db_name_upper]
            self.host = '172.16.22.44'
            self.port = '1521'
            self.service_name = config['service_name']
            self.user = config['user']
            self.password = config['password']
            self.connection_string = f'oracle+cx_oracle://{self.user}:{self.password}@{self.host}:{self.port}/?service_name={self.service_name}'
            self.engine = create_engine(self.connection_string)
            self.db_type = 'oracle'
        elif db_name_upper == 'VERTICA':
            self.conn_info = {
                'host': os.getenv('VERTICA_HOST'),
                'port': int(os.getenv('VERTICA_PORT')),
                'user': os.getenv('VERTICA_USER'),
                'password': os.getenv('VERTICA_PASSWORD'),
                'database': os.getenv('VERTICA_DATABASE'),
            }
            self.db_type = 'vertica'
        else:
            raise ValueError(f"Database configuration for '{db_name}' not found.")

    def query(self, sql_query):
        logging.info(f"Database query: {sql_query}")
        if self.db_type == 'oracle':
            with self.engine.connect() as connection:
                result = pd.read_sql_query(sql_query, connection)
            return result
        elif self.db_type == 'vertica':
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
        else:
            raise ValueError("Query method called for unsupported database type.")
