import logging
from typing import Dict, Tuple

from message_processing.message_processor import MessageProcessor
from query_generation.query_generator import QueryGenerator
from query_generation.sql_validator import SQLValidator


class NLMessageProcessor(MessageProcessor):
    """
    Extended MessageProcessor that can handle natural language queries in addition to SQL queries.
    Uses the Mistral AI API through the QueryGenerator component to convert natural language to SQL.
    """

    def __init__(self):
        """
        Initialize the NLMessageProcessor with the necessary components.
        """
        super().__init__()  # Initialize the base MessageProcessor
        self.query_generator = QueryGenerator()
        self.sql_validator = SQLValidator()
        self.logger = logging.getLogger(__name__)
    
    async def process_message(self, message: str, channel_id: str) -> str:
        """
        Overrides the base process_message to handle natural language messages.
        
        Args:
            message: The message from Slack (could be SQL or natural language).
            channel_id: The Slack channel ID.
            
        Returns:
            The response message to send to Slack.
        """
        logging.info(f"Processing message with NL capability for channel: {channel_id}")
        logging.debug(f"Received message: {message}")
        
        try:
            # Parse the message to extract db_type, query text, and debug mode
            db_type, text, is_debug_mode = self.parser.parse_message(message)
            logging.info(f"Parsed message. DB Type: {db_type}, Text: {text}, Debug Mode: {is_debug_mode}")
            
            if is_debug_mode:
                logging.info("Debug mode is active based on parser.")

            # If text is empty, return a help message
            if not text:
                return "I'm SQLoslav, your SQL assistant! Please ask me a question or provide a SQL query to execute."
            
            # Add extra debug logging to see if NL detection works
            is_natural_language = self.query_generator.is_natural_language(text)
            logging.info(f"Is natural language? {is_natural_language}")
            
            # Check if the input is natural language or SQL
            if is_natural_language:
                logging.info("Detected natural language query, generating SQL")
                
                try:
                    # Convert natural language to SQL
                    sql_query, metadata = self.query_generator.generate_sql_from_natural_language(text)
                    
                    # Log the generated SQL and metadata
                    logging.info(f"Generated SQL from natural language: {sql_query}")
                    logging.debug(f"Query generation metadata: {metadata}")
                    
                    # Validate the generated SQL query
                    is_valid, validation_results = self.sql_validator.validate_query(sql_query)
                    
                    if not is_valid:
                        # If validation fails, return an error message
                        error_message = f"Generated SQL query failed validation: {', '.join(validation_results['issues'])}"
                        logging.warning(error_message)
                        return error_message
                    
                    # If we have an explanation in the metadata, include it in the message
                    explanation = metadata.get('explanation', '')
                    
                    # Format a message to send to the user showing the generated SQL
                    generated_message = f"Translating your question: \"{text}\"\n\n"
                    generated_message += f"Generated SQL Query:\n```{sql_query}```\n\n"
                    
                    if explanation:
                        generated_message += f"Explanation: {explanation}\n\n"
                        
                    generated_message += "Executing the generated query now...\n"
                    
                    # Send an initial message with the generated SQL only if in debug mode
                    if is_debug_mode:
                        await self.send_message_to_slack(generated_message, channel_id)
                    
                    # Use the existing SQL execution flow with the generated query
                    result_df = self.sql_executor.execute_sql(sql_query, db_type)
                    self.log_dataframe_info(result_df)
                    
                    if result_df.empty:
                        logging.info("Query executed successfully but returned no results.")
                        return self.format_no_results_message(sql_query)
                    
                    # Summarize and save the results
                    _, file_path = self.sql_executor.summarize_and_save(result_df)
                    
                    try:
                        # Upload the results file to Slack
                        await self.slack_uploader.upload_file_to_slack(file_path, channel_id)
                        return ""  # Return empty string to avoid sending another message
                    except Exception as e:
                        error_message = self.error_handler.handle_error(e, "uploading file to Slack", channel_id)
                        return error_message
                
                except RuntimeError as e:
                    if "model_dump" in str(e):
                        error_message = "There's an API compatibility issue with the Mistral AI library. Please contact the administrator."
                        logging.error(f"Mistral AI API compatibility error: {str(e)}", exc_info=True)
                        return error_message
                    else:
                        error_message = self.error_handler.handle_error(e, "generating SQL query", channel_id)
                        return error_message
                except Exception as e:
                    error_message = self.error_handler.handle_error(e, "processing natural language query", channel_id)
                    return error_message
                
            else:
                # It's a regular SQL query, use the standard processing from base class
                logging.info("Detected SQL query, using standard processing")
                # The base class process_message will now also need to handle the is_debug_mode
                # if its output needs to be conditional. For now, we pass the original full message
                # and let the modified parser in the superclass call handle it.
                # However, super().process_message itself might not be designed to accept is_debug_mode directly.
                # We will modify super().process_message to also use the new parser output.
                return await super().process_message(message, channel_id) # message is the original raw message
                
        except Exception as e:
            error_message = self.error_handler.handle_error(e, "processing message with NL capability", channel_id)
            return error_message
            
    async def send_message_to_slack(self, message: str, channel_id: str) -> None:
        """
        Helper method to send a message to a Slack channel.
        
        Args:
            message: The message text to send.
            channel_id: The Slack channel ID.
        """
        try:
            await self.slack_uploader.send_message_to_channel(message, channel_id)
            logging.info(f"Sent message to Slack channel: {channel_id}")
        except Exception as e:
            logging.error(f"Error sending message to Slack: {str(e)}", exc_info=True) 