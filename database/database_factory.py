from database.vertica_database import VerticaDatabase
from database.oracle_database import OracleDatabase


class DatabaseFactory:
    @staticmethod
    def get_database(db_type: str):
        if db_type == 'VERTICA':
            return VerticaDatabase()
        elif db_type in ['SINONIMI', 'SHOPSTER', 'VIRGA_TEST', 'VIRGA']:
            return OracleDatabase(db_type)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
