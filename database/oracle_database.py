import pandas as pd
from sqlalchemy import create_engine
import os
import logging
from database.base_database import BaseDatabase


class OracleDatabase(BaseDatabase):
    def __init__(self, db_name: str):
        super().__init__('oracle')
        db_config = {
            'sinonimi': {
                'service_name': os.getenv('ORACLE_SINONIMI_SERVICE_NAME'),
                'user': os.getenv('ORACLE_SINONIMI_USER'),
                'password': os.getenv('ORACLE_SINONIMI_PASSWORD')
            },
            'shopster': {
                'service_name': os.getenv('ORACLE_SHOPSTER_SERVICE_NAME'),
                'user': os.getenv('ORACLE_SHOPSTER_USER'),
                'password': os.getenv('ORACLE_SHOPSTER_PASSWORD')
            },
            'virga_test': {
                'service_name': os.getenv('ORACLE_VIRGA_TEST_SERVICE_NAME'),
                'user': os.getenv('ORACLE_VIRGA_TEST_USER'),
                'password': os.getenv('ORACLE_VIRGA_TEST_PASSWORD')
            },
            'virga': {
                'service_name': os.getenv('ORACLE_VIRGA_SERVICE_NAME'),
                'user': os.getenv('ORACLE_VIRGA_USER'),
                'password': os.getenv('ORACLE_VIRGA_PASSWORD')
            }
        }
        config = db_config.get(db_name.lower())
        if not config:
            raise ValueError(f"Database configuration for '{db_name}' not found.")

        self.host = os.getenv('ORACLE_HOST')
        self.port = os.getenv('ORACLE_PORT')
        self.service_name = config['service_name']
        self.user = config['user']
        self.password = config['password']
        self.connection_string = f'oracle+cx_oracle://{self.user}:{self.password}@{self.host}:{self.port}/?service_name={self.service_name}'
        self.engine = create_engine(self.connection_string)
        logging.info(f"Initialized OracleDatabase for {db_name}")

    def query(self, sql_query: str):
        logging.info(f"Database query: {sql_query}")
        with self.engine.connect() as connection:
            result = pd.read_sql_query(sql_query, connection)
        return result
