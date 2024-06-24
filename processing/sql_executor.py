import logging
from database.database_factory import DatabaseFactory
from processing.data_frame_handler import DataFrameHandler


class SQLExecutor:
    def __init__(self):
        self.df_handler = DataFrameHandler()

    @staticmethod
    def execute_sql(sql_query: str, db_type: str):
        logging.info(f"Executing SQL query: {sql_query}")

        db = DatabaseFactory.get_database(db_type)
        result_df = db.query(sql_query)
        logging.info(f"Query result DataFrame: {result_df}")
        return result_df

    def summarize_and_save(self, result_df):
        summary_df = self.df_handler.summarize_dataframe(result_df)
        file_path = self.df_handler.save_dataframe_to_file(result_df)
        return summary_df, file_path
