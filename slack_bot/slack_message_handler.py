import logging
from slack_sdk import WebClient
from message_processing.message_processor import MessageProcessor
from data.data_base import Database

class SlackMessageHandler:
    def __init__(self, client: WebClient):
        self.client = client
        self.processor = MessageProcessor()
        self.db = Database('VERTICA')  # Initialize Database instance for Vertica

    async def handle(self, event):
        channel_id = event.get('channel')
        user_message = event.get('text', '')

        if user_message:
            response_message = self.processor.process_message(user_message, self.db, channel_id)
            try:
                self.client.chat_postMessage(channel=channel_id, text=response_message)
                logging.info(f"Message sent: {response_message}")
            except Exception as e:
                logging.error(f"Slack API error: {e}")
        else:
            logging.warning("Received a message event without text content.")
