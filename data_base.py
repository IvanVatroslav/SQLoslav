import pandas as pd
from sqlalchemy import create_engine
import vertica_python
import os
from dotenv import load_dotenv
import logging

load_dotenv()  # Load environment variables from .env file


class Database:
    def __init__(self, db_name):
        db_name_upper = db_name.upper()
        if db_name_upper == 'SINONIMI':
            self.host = '172.16.22.44'
            self.port = '1521'
            self.service_name = os.getenv('ORACLE_SINONIMI_SERVICE_NAME')
            self.user = os.getenv('ORACLE_SINONIMI_USER')
            self.password = os.getenv('ORACLE_SINONIMI_PASSWORD')
        elif db_name_upper == 'SHOPSTER':
            self.host = '172.16.22.44'
            self.port = '1521'
            self.service_name = os.getenv('ORACLE_SHOPSTER_SERVICE_NAME')
            self.user = os.getenv('ORACLE_SHOPSTER_USER')
            self.password = os.getenv('ORACLE_SHOPSTER_PASSWORD')
        elif db_name_upper == 'VIRGA_TEST':
            self.host = '172.16.22.44'
            self.port = '1521'
            self.service_name = os.getenv('ORACLE_VIRGA_TEST_SERVICE_NAME')
            self.user = os.getenv('ORACLE_VIRGA_TEST_USER')
            self.password = os.getenv('ORACLE_VIRGA_TEST_PASSWORD')
        elif db_name_upper == 'VIRGA':
            self.host = '172.16.22.44'
            self.port = '1521'
            self.service_name = os.getenv('ORACLE_VIRGA_SERVICE_NAME')
            self.user = os.getenv('ORACLE_VIRGA_USER')
            self.password = os.getenv('ORACLE_VIRGA_PASSWORD')
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

        if db_name_upper in ['SINONIMI', 'SHOPSTER', 'VIRGA_TEST', 'VIRGA']:
            self.connection_string = f'oracle+cx_oracle://{self.user}:{self.password}@{self.host}:{self.port}/?service_name={self.service_name}'
            self.engine = create_engine(self.connection_string)
            self.db_type = 'oracle'

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
