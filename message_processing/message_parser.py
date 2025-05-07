class MessageParser:
    def __init__(self):
        pass

    def parse_message(self, message: str):
        lines = message.strip().split('\n')
        if len(lines) < 2:
            raise ValueError("Invalid message format. Expected at least two lines.")

        trigger_line = lines[0].strip().lower()
        query = '\n'.join(lines[1:]).strip()

        # Check for SQLoslav trigger word (case insensitive)
        if trigger_line == "sqloslav":
            # Default to PostgreSQL for SQLoslav
            db_type = "POSTGRES"
        else:
            raise ValueError("Invalid trigger word. Expected 'SQLoslav'.")

        clean_query = self.clean_query(query)
        return db_type, clean_query

    @staticmethod
    def clean_query(query: str) -> str:
        return query.strip('`')

    @staticmethod
    def prepare_slack_payload(markdown_table: str) -> str:
        return f"```\n{markdown_table}\n```"
