import pandas as pd
import logging


class DataFrameHandler:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def summarize_dataframe(self, df: pd.DataFrame, max_rows: int = 5, max_columns: int = 5) -> pd.DataFrame:
        logging.info(f"Summarizing DataFrame with max_rows={max_rows}, max_columns={max_columns}")
        if df.shape[0] <= max_rows:
            summary = df
        else:
            summary = pd.concat([df.head(max_rows), df.tail(max_rows)])
        if df.shape[1] > max_columns:
            summary = summary.iloc[:, :max_columns]
        logging.info(f"DataFrame summary created:\n{summary}")
        return summary

    def convert_df_to_markdown(self, df: pd.DataFrame) -> str:
        logging.info("Converting DataFrame to Markdown format")
        markdown = df.to_markdown(index=False)
        logging.info(f"DataFrame converted to Markdown:\n{markdown}")
        return markdown

    def save_dataframe_to_file(self, df: pd.DataFrame, file_format: str = 'csv') -> str:
        file_name = f"query_result.{file_format}"
        try:
            logging.info(f"Saving DataFrame to file: {file_name} in format: {file_format}")
            if file_format == 'csv':
                df.to_csv(file_name, index=False)
            elif file_format == 'json':
                df.to_json(file_name, orient='records', lines=True)
            elif file_format == 'excel':
                df.to_excel(file_name, index=False)
            logging.info(f"DataFrame saved to file: {file_name}")
            return file_name
        except Exception as e:
            logging.error(f"Error saving DataFrame to file: {e}")
            raise
