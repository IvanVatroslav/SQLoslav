import logging
from data_base import Database
from data_frame_handler import DataFrameHandler
from slack_uploader import SlackUploader
from error_handler import ErrorHandler
import os


class MessageProcessor:
    def __init__(self):
        self.df_handler = DataFrameHandler()
        self.slack_uploader = SlackUploader(token=os.getenv('SLACK_BOT_TOKEN'))
        self.error_handler = ErrorHandler()

    def process_message(self, message: str, db: Database, channel_id: str) -> str:
        logging.info(f"Processing message for channel: {channel_id}")
        if message.lower().startswith("sql, vertica"):
            sql_query = message[len("SQL, vertica"):].strip()
            if not sql_query:
                return "No SQL query provided."

            try:
                clean_query = self.clean_query(sql_query)
                logging.info(f"Executing SQL query: {clean_query}")
                result_df = db.query(clean_query)
                logging.info(f"Query result DataFrame: {result_df}")

                if result_df.empty:
                    logging.info("Query executed successfully but returned no results.")
                    return f"Query executed successfully but returned no results.\nSQL query: ```{sql_query}```"

                summary_df = self.df_handler.summarize_dataframe(result_df)
                markdown_table = self.df_handler.convert_df_to_markdown(summary_df)
                slack_data = self.prepare_slack_payload(markdown_table)

                try:
                    file_path = self.df_handler.save_dataframe_to_file(result_df)
                    logging.info(f"Data saved to file: {file_path}")
                except Exception as e:
                    error_message = self.error_handler.handle_error(e, "saving data to file", channel_id)
                    return error_message

                try:
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

    def clean_query(self, query: str) -> str:
        return query.strip('`')

    def prepare_slack_payload(self, markdown_table: str) -> str:
        return f"```\n{markdown_table}\n```"
