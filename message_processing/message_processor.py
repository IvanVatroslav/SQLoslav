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
            db_type, sql_query, is_debug_mode = self.parser.parse_message(message)
            logging.info(f"Parsed message. DB Type: {db_type}, SQL Query: {sql_query}, Debug Mode: {is_debug_mode}")

            if not sql_query:
                return "Please provide a SQL query to execute after 'SQLoslav' or 'SQLoslav, debug'."

            result_df = self.sql_executor.execute_sql(sql_query, db_type)
            self.log_dataframe_info(result_df)

            if result_df.empty:
                logging.info("Query executed successfully but returned no results.")
                if is_debug_mode:
                    return self.format_no_results_message(sql_query)
                else:
                    return "Query executed successfully but returned no results."

            _, file_path = self.sql_executor.summarize_and_save(result_df)

            try:
                await self.slack_uploader.upload_file_to_slack(file_path, channel_id)
                if is_debug_mode:
                    return f"Query successful. Results are in the attached file: {os.path.basename(file_path)}"
                else:
                    return ""
            except Exception as e:
                error_message = self.error_handler.handle_error(e, "uploading file to Slack", channel_id)
                return error_message

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
                f"SQL query (for debugging): ```{sql_query}```\n"
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
