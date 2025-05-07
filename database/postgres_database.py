import pandas as pd
from sqlalchemy import create_engine, text
import os
import logging
from database.base_database import BaseDatabase


class PostgresDatabase(BaseDatabase):
    def __init__(self):
        super().__init__('postgres')
        
        # Get environment variables with defaults
        postgres_host = os.getenv('POSTGRES_HOST', 'postgres')
        postgres_port = os.getenv('POSTGRES_PORT', '5432')
        postgres_user = os.getenv('POSTGRES_USER', 'admin')
        postgres_password = os.getenv('POSTGRES_PASSWORD', 'admin')
        postgres_db = os.getenv('POSTGRES_DB', 'sqloslav_dwh')
        
        # Create connection string
        self.connection_string = f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}'
        self.engine = create_engine(self.connection_string)
        
        # Log connection info with password masked
        safe_conn_string = self.connection_string.replace(postgres_password, '********')
        logging.info(f"Initialized PostgresDatabase with connection: {safe_conn_string}")

    def query(self, sql_query: str):
        logging.info(f"Database query: {sql_query}")
        try:
            # Remove trailing semicolon if present
            sql_query = sql_query.rstrip(';')
            
            with self.engine.connect() as connection:
                # Use text() to create a proper SQL statement
                stmt = text(sql_query)
                result = pd.read_sql_query(stmt, connection)
                logging.info(f"Query returned {len(result)} rows.")
                return result
        except Exception as e:
            logging.error(f"Error executing PostgreSQL query: {e}")
            raise Exception(f"PostgreSQL database error: {e}") 