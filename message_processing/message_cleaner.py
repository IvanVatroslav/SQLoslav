class MessageCleaner:
    @staticmethod
    def clean_query(query: str) -> str:
        return query.strip('`')
