import logging
import os
from slack_sdk import WebClient
from fastapi import Request
from dotenv import load_dotenv
from slack_bot.event_handler import EventHandler

load_dotenv(dotenv_path='config/.env')


class SlackBot:
    def __init__(self):
        self.client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
        self.event_handler = EventHandler(self.client)
        self.processed_events = set()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    async def handle_event(self, request: Request):
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
        await self.event_handler.handle(event)
        return {"status": "ok"}
