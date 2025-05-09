from .base_database import BaseDatabase
from .oracle_database import OracleDatabase
from .vertica_database import VerticaDatabase
from .postgres_database import PostgresDatabase


def get_database(db_name):
    db_name_upper = db_name.upper()
    if db_name_upper in ['SINONIMI', 'SHOPSTER', 'VIRGA_TEST', 'VIRGA']:
        return OracleDatabase(db_name)
    elif db_name_upper == 'VERTICA':
        return VerticaDatabase()
    elif db_name_upper == 'POSTGRES':
        return PostgresDatabase()
    else:
        raise ValueError(f"Database configuration for '{db_name}' not found.")
