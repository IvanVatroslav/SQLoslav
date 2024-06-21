import pandas as pd
import logging
import os
from datetime import datetime


class DataFrameHandler:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    @staticmethod
    def summarize_dataframe(df: pd.DataFrame, max_rows: int = 5, max_columns: int = 5) -> pd.DataFrame:
        logging.info(f"Summarizing DataFrame with max_rows={max_rows}, max_columns={max_columns}")
        if df.shape[0] <= max_rows:
            summary = df
        else:
            summary = pd.concat([df.head(max_rows), df.tail(max_rows)])
        if df.shape[1] > max_columns:
            summary = summary.iloc[:, :max_columns]
        logging.info(f"DataFrame summary created:\n{summary}")
        return summary

    @staticmethod
    def convert_df_to_markdown(df: pd.DataFrame) -> str:
        logging.info("Converting DataFrame to Markdown format")
        markdown = df.to_markdown(index=False)
        logging.info(f"DataFrame converted to Markdown:\n{markdown}")
        return markdown

    @staticmethod
    def save_dataframe_to_file(df: pd.DataFrame, prefix: str = "query_result") -> str:
        logging.info("Saving DataFrame to file")
        try:
            # Ensure the 'output' directory exists
            os.makedirs('output', exist_ok=True)

            # Generate a unique filename using the current timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{prefix}_{timestamp}.csv"
            file_path = os.path.join('output', file_name)

            # Save the DataFrame to a CSV file
            df.to_csv(file_path, index=False, encoding='utf-8')

            logging.info(f"DataFrame saved successfully to {file_path}")
            return file_path
        except Exception as e:
            logging.error(f"Error saving DataFrame to file: {str(e)}")
            return None
