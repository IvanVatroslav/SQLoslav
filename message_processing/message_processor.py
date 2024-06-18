import logging
import os
from data.data_base import Database
from slack_uploader.slack_uploader import SlackUploader
from error_handling.error_handler import ErrorHandler
from message_processing.message_cleaner import MessageCleaner
from message_processing.slack_payload_preparer import SlackPayloadPreparer
from message_processing.sql_executor import SQLExecutor


class MessageProcessor:
    def __init__(self):
        self.sql_executor = SQLExecutor()
        self.slack_uploader = SlackUploader(token=os.getenv('SLACK_BOT_TOKEN'))
        self.error_handler = ErrorHandler()
        self.message_cleaner = MessageCleaner()
        self.slack_payload_preparer = SlackPayloadPreparer()

    def process_message(self, message: str, db: Database, channel_id: str) -> str:
        logging.info(f"Processing message for channel: {channel_id}")
        if message.lower().startswith("sql, vertica"):
            sql_query = message[len("SQL, vertica"):].strip()
            if not sql_query:
                return "No SQL query provided."

            try:
                clean_query = self.message_cleaner.clean_query(sql_query)
                result_df = self.sql_executor.execute_sql(clean_query, db)

                if result_df.empty:
                    logging.info("Query executed successfully but returned no results.")
                    return f"Query executed successfully but returned no results.\nSQL query: ```{clean_query}```"

                markdown_table, file_path = self.slack_payload_preparer.summarize_and_save(result_df)
                slack_data = self.slack_payload_preparer.prepare_slack_payload(markdown_table)

                try:
                    logging.info(f"Data saved to file: {file_path}")
                    logging.info(f"Attempting to upload file to Slack channel: {channel_id}")
                    file_url = self.slack_uploader.upload_file_to_slack(file_path, channel_id)
                    logging.info(f"File uploaded successfully: {file_url}")
                    slack_data += f"\nFull results: {file_url}"
                except Exception as e:
                    error_message = self.error_handler.handle_error(e, "uploading file to Slack", channel_id)
                    slack_data += f"\n{error_message}"

                logging.info(f"Prepared Slack payload: {slack_data}")
                return slack_data

            except Exception as e:
                error_message = self.error_handler.handle_error(e, "executing query", channel_id)
                return error_message
        else:
            return f"You said: {message}"
