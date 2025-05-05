import pandas as pd
import logging
import os
from datetime import datetime


class DataFrameHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Use the DATA_DIR environment variable or default to 'data'
        self.data_dir = os.getenv('DATA_DIR', 'data')
        # Ensure the data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        self.logger.info(f"Using data directory: {self.data_dir}")

    def summarize_dataframe(self, df: pd.DataFrame, max_rows: int = 5, max_columns: int = 5) -> pd.DataFrame:
        self.logger.info(f"Summarizing DataFrame with max_rows={max_rows}, max_columns={max_columns}")
        if df.shape[0] <= max_rows:
            summary = df
        else:
            summary = pd.concat([df.head(max_rows), df.tail(max_rows)])
        if df.shape[1] > max_columns:
            summary = summary.iloc[:, :max_columns]
        self.logger.info(f"DataFrame summary created with shape {summary.shape}")
        return summary

    def save_dataframe_to_file(self, df: pd.DataFrame, prefix: str = "query_result") -> str:
        self.logger.info("Saving DataFrame to file")
        try:
            # Generate a unique filename using the current timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{prefix}_{timestamp}.csv"
            file_path = os.path.join(self.data_dir, file_name)

            # Save the DataFrame to a CSV file
            df.to_csv(file_path, index=False, encoding='utf-8')

            self.logger.info(f"DataFrame saved successfully to {file_path}")
            return file_path
        except Exception as e:
            self.logger.error(f"Error saving DataFrame to file: {str(e)}")
            raise e
