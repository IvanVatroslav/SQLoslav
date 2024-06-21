class MessageParser:
    def __init__(self):
        pass

    def parse_message(self, message: str):
        lines = message.strip().split('\n')
        if len(lines) < 2:
            raise ValueError("Invalid message format. Expected at least two lines.")

        db_type_line = lines[0].strip().lower()
        query = '\n'.join(lines[1:]).strip()

        if db_type_line.startswith("sql,"):
            db_type = db_type_line.split(",")[1].strip().upper()
        else:
            raise ValueError("Invalid database type format.")

        clean_query = self.clean_query(query)
        return db_type, clean_query

    @staticmethod
    def clean_query(query: str) -> str:
        return query.strip('`')

    @staticmethod
    def prepare_slack_payload(markdown_table: str) -> str:
        return f"```\n{markdown_table}\n```"
