from database.vertica_database import VerticaDatabase
from database.oracle_database import OracleDatabase
from database.postgres_database import PostgresDatabase


class DatabaseFactory:
    @staticmethod
    def get_database(db_type: str):
        if db_type == 'VERTICA':
            return VerticaDatabase()
        elif db_type in ['SINONIMI', 'SHOPSTER', 'VIRGA_TEST', 'VIRGA']:
            return OracleDatabase(db_type)
        elif db_type == 'POSTGRES':
            return PostgresDatabase()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
