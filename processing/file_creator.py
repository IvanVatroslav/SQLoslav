import pandas as pd
import logging
import os


class FileCreator:
    def __init__(self):
        self.output_directory = 'output'
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def create_file(self, df: pd.DataFrame, file_format: str = 'csv') -> str:
        file_name = f"query_result.{file_format}"
        file_path = os.path.join(self.output_directory, file_name)

        try:
            logging.info(f"Saving DataFrame to file: {file_path} in format: {file_format}")
            if file_format == 'csv':
                df.to_csv(file_path, index=False)
            elif file_format == 'json':
                df.to_json(file_path, orient='records', lines=True)
            elif file_format == 'excel':
                df.to_excel(file_path, index=False)
            else:
                raise ValueError(f"Unsupported file format: {file_format}")
            logging.info(f"DataFrame saved to file: {file_path}")
            return file_path
        except Exception as e:
            logging.error(f"Error saving DataFrame to file: {e}")
            raise
