import os
import logging
from fastapi import HTTPException, Request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from message_processor import MessageProcessor

load_dotenv()  # Load environment variables from .env file

class SlackBot:
    def __init__(self):
        self.client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
        self.processor = MessageProcessor()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)

    async def handle_event(self, request: Request):
        data = await request.json()
        logging.info(f"Received request: {data}")

        if data['type'] == "url_verification":
            logging.info(f"Challenge received: {data['challenge']}")
            return {"challenge": data['challenge']}

        if data.get('event') and data['event'].get('type') == 'message' and 'bot_id' not in data['event']:
            user_message = data['event']['text']
            channel_id = data['event']['channel']

            logging.info(f"Message received: {user_message}")
            logging.info(f"Channel ID: {channel_id}")

            response_message = self.processor.process_message(user_message)

            try:
                self.client.chat_postMessage(channel=channel_id, text=response_message)
                logging.info(f"Message sent: {response_message}")
            except SlackApiError as e:
                logging.error(f"Slack API error: {e.response['error']}")
                raise HTTPException(status_code=400, detail=f"Slack API error: {e.response['error']}")

        return {"status": "ok"}
