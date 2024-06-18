class SlackPayloadPreparer:
    @staticmethod
    def prepare_slack_payload(markdown_table: str) -> str:
        return f"```\n{markdown_table}\n```"
