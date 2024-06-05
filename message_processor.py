import pandas as pd
import logging
from data_base import Database

class MessageProcessor:
    def process_message(self, message: str, db: Database) -> str:
        if message.lower().startswith("sql, vertica"):
            sql_query = message[len("SQL, vertica"):].strip()
            if not sql_query:
                return "No SQL query provided."

            try:
                # Clean the query to remove Slack-specific formatting while preserving SQL syntax
                clean_query = self.clean_query(sql_query)

                logging.info(f"Executing SQL query: {clean_query}")
                result_df = db.query(clean_query)
                logging.info(f"Query result DataFrame: {result_df}")

                if result_df.empty:
                    logging.info("Query executed successfully but returned no results.")
                    return f"Query executed successfully but returned no results.\nSQL query: ```{sql_query}```"

                markdown_table = self.convert_df_to_markdown(result_df)
                slack_data = self.prepare_slack_payload(markdown_table)
                logging.info(f"Prepared Slack payload: {slack_data}")
                return slack_data

            except Exception as e:
                logging.error(f"Error executing query: {e}")
                return f"Error executing query: {e}"
        else:
            return f"You said: {message}"

    def clean_query(self, query: str) -> str:
        # Remove triple backticks used for code blocks in Slack messages
        return query.strip('`')

    def convert_df_to_markdown(self, df: pd.DataFrame) -> str:
        return df.to_markdown(index=False)

    def prepare_slack_payload(self, markdown_table: str) -> str:
        return f"```\n{markdown_table}\n```"
