import os
import logging
from fastapi import Request, HTTPException
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from message_processor import MessageProcessor
from data_base import Database

load_dotenv()  # Load environment variables from .env file

class SlackBot:
    def __init__(self):
        self.client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
        self.processor = MessageProcessor()
        self.setup_logging()
        self.db = Database('VERTICA')  # Initialize Database instance for Vertica
        self.processed_events = set()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    async def handle_event(self, request: Request, channel_id: str):
        data = await request.json()
        logging.info(f"Received request: {data}")

        event_id = data.get('event_id')
        if event_id in self.processed_events:
            logging.info(f"Event {event_id} has already been processed. Skipping.")
            return {"status": "ok"}

        self.processed_events.add(event_id)

        if data['type'] == "url_verification":
            logging.info(f"Challenge received: {data['challenge']}")
            return {"challenge": data['challenge']}

        event = data.get('event', {})
        if event.get('type') == 'message' and 'bot_id' not in event:
            user_message = event.get('text', '')
            logging.info(f"Message received: {user_message}")
            logging.info(f"Channel ID: {channel_id}")

            if user_message:
                response_message = self.processor.process_message(user_message, self.db, channel_id)
                try:
                    self.client.chat_postMessage(channel=channel_id, text=response_message)
                    logging.info(f"Message sent: {response_message}")
                except SlackApiError as e:
                    logging.error(f"Slack API error: {e.response['error']}")
                    raise HTTPException(status_code=400, detail=f"Slack API error: {e.response['error']}")
            else:
                logging.warning("Received a message event without text content.")
        else:
            logging.warning("Received an unsupported event type or a message from a bot.")

        return {"status": "ok"}
