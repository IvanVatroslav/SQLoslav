class MessageParser:
    def __init__(self):
        pass

    def parse_message(self, message: str):
        message_lower = message.strip().lower()
        text_content = message.strip()
        is_debug_mode = False
        db_type = "POSTGRES"  # Default for SQLoslav

        # Order of checks is important: check for "sqloslav, debug" first
        if message_lower.startswith("sqloslav, debug"):
            is_debug_mode = True
            # Extract text after "sqloslav, debug " (note the space)
            # Original casing of the query is preserved from text_content
            prefix_len = len("sqloslav, debug ")
            if len(text_content) > prefix_len:
                query_text = text_content[prefix_len:].strip()
            else: # Handles "sqloslav, debug" with nothing after
                query_text = ""
            
        elif message_lower.startswith("sqloslav"):
            # Handles "sqloslav" and "sqloslav " (note the space)
            # Original casing of the query is preserved from text_content
            prefix_len = len("sqloslav ")
            if message_lower == "sqloslav": # Just "sqloslav"
                query_text = ""
            elif len(text_content) > prefix_len: # "sqloslav query..."
                query_text = text_content[prefix_len:].strip()
            else: # Handles "sqloslav " with nothing after (edge case, strip would make it same as just "sqloslav")
                query_text = "" # Should effectively be caught by message_lower == "sqloslav" after strip
        else:
            # If it doesn't start with "sqloslav" at all,
            # consider it as direct natural language text or an invalid command.
            # For NLMessageProcessor, this means the whole message is the 'text'.
            # We should not raise an error here if we want NLProcessor to handle non-prefixed messages.
            # Let's assume for now that if it's not prefixed, it's all query_text and not debug mode.
            query_text = text_content 
            # db_type remains POSTGRES, or could be made None if not SQLoslav-triggered
            # For simplicity with current NL flow, let's keep db_type POSTGRES.
            # And it's not debug mode if not explicitly triggered.

        clean_query = self.clean_query(query_text)
        return db_type, clean_query, is_debug_mode

    @staticmethod
    def clean_query(query: str) -> str:
        return query.strip('`')

    @staticmethod
    def prepare_slack_payload(markdown_table: str) -> str:
        return f"```\n{markdown_table}\n```"
