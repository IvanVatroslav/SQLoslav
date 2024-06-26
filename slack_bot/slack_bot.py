# slack_bot/slack_bot.py

import logging
from slack_sdk.web.async_client import AsyncWebClient
from dotenv import load_dotenv
from slack_bot.event_handler import EventHandler
from slack_bot.logger import LoggerSetup  # Import LoggerSetup
import os

load_dotenv()


class SlackBot:
    def __init__(self):
        LoggerSetup.setup_logging()  # Set up logging first
        self.client = AsyncWebClient(token=os.getenv('SLACK_BOT_TOKEN'))
        self.event_handler = EventHandler(self.client)
        self.processed_events = set()

    async def handle_event(self, data: dict):
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
        await self.event_handler.handle_event(event)
        return {"status": "ok"}
