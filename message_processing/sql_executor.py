import logging
from data.data_base import Database
from data.data_frame_handler import DataFrameHandler


class SQLExecutor:
    def __init__(self):
        self.df_handler = DataFrameHandler()

    def execute_sql(self, sql_query: str, db: Database):
        logging.info(f"Executing SQL query: {sql_query}")
        result_df = db.query(sql_query)
        logging.info(f"Query result DataFrame: {result_df}")
        return result_df

    def summarize_and_save(self, result_df):
        summary_df = self.df_handler.summarize_dataframe(result_df)
        markdown_table = self.df_handler.convert_df_to_markdown(summary_df)
        file_path = self.df_handler.save_dataframe_to_file(result_df)
        return markdown_table, file_path
