import logging
import os
import pandas as pd
from message_processing.message_parser import MessageParser
from processing.sql_executor import SQLExecutor
from slack_uploader.slack_uploader import SlackUploader
from error_handling.error_handler import ErrorHandler


class MessageProcessor:
    def __init__(self):
        self.sql_executor = SQLExecutor()
        self.slack_uploader = SlackUploader(token=os.getenv('SLACK_BOT_TOKEN'))
        self.error_handler = ErrorHandler()
        self.parser = MessageParser()
        logging.getLogger().setLevel(logging.DEBUG)

    async def process_message(self, message: str, channel_id: str) -> str:
        logging.info(f"Processing message for channel: {channel_id}")
        logging.debug(f"Received message: {message}")

        try:
            db_type, sql_query = self.parser.parse_message(message)
            logging.info(f"Parsed message. DB Type: {db_type}, SQL Query: {sql_query}")

            result_df = self.sql_executor.execute_sql(sql_query, db_type)
            self.log_dataframe_info(result_df)

            if result_df.empty:
                logging.info("Query executed successfully but returned no results.")
                return self.format_no_results_message(sql_query)

            markdown_table, file_path = self.sql_executor.summarize_and_save(result_df)
            slack_data = self.parser.prepare_slack_payload(markdown_table)

            try:
                file_url = await self.slack_uploader.upload_file_to_slack(file_path, channel_id)
                slack_data += f"\nFull results: {file_url}"

                # Verify the uploaded file
                verification_result = await self.verify_uploaded_file(file_url, file_path)
                if not verification_result:
                    slack_data += "\nWarning: The uploaded file could not be verified. It may not be accessible."
            except Exception as e:
                error_message = self.error_handler.handle_error(e, "uploading file to Slack", channel_id)
                slack_data += f"\n{error_message}"

            logging.info(f"Prepared Slack payload: {slack_data}")
            return slack_data

        except Exception as e:
            error_message = self.error_handler.handle_error(e, "processing message", channel_id)
            return error_message

    @staticmethod
    def log_dataframe_info(df: pd.DataFrame):
        logging.info(f"DataFrame info:")
        logging.info(f"  Shape: {df.shape}")
        logging.info(f"  Columns: {df.columns.tolist()}")
        logging.info(f"  Data types:\n{df.dtypes}")
        if not df.empty:
            logging.debug(f"  First few rows:\n{df.head().to_string()}")

    @staticmethod
    def format_no_results_message(sql_query: str) -> str:
        return (f"Query executed successfully but returned no results.\n"
                f"SQL query: ```{sql_query}```\n"
                f"Please check your query and try again.")

    async def verify_uploaded_file(self, file_url: str, original_file_path: str) -> bool:
        try:
            downloaded_file_path = await self.slack_uploader.download_file(file_url,
                                                                           os.path.basename(original_file_path))

            original_size = os.path.getsize(original_file_path)
            downloaded_size = os.path.getsize(downloaded_file_path)

            if original_size != downloaded_size:
                logging.warning(
                    f"Uploaded file size mismatch. Original: {original_size}, Downloaded: {downloaded_size}")
                return False

            # Compare file contents
            with open(original_file_path, 'rb') as f1, open(downloaded_file_path, 'rb') as f2:
                if f1.read() != f2.read():
                    logging.warning("File content mismatch between original and downloaded file")
                    return False

            logging.info("Uploaded file verified successfully")
            return True

        except Exception as e:
            logging.error(f"Error verifying uploaded file: {str(e)}", exc_info=True)
            return False
        finally:
            if 'downloaded_file_path' in locals() and os.path.exists(downloaded_file_path):
                os.remove(downloaded_file_path)  # Clean up the downloaded file
