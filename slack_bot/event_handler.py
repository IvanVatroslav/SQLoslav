# slack_bot/event_handler.py

import logging
from slack_sdk.web.async_client import AsyncWebClient
from message_processing.message_handler import MessageHandler
from message_processing.nl_message_handler import NLMessageHandler  # Import the new handler
from slack_bot.slack_file_handler import SlackFileHandler
from slack_bot.logger import LoggerSetup  # Import LoggerSetup


class EventHandler:
    def __init__(self, client: AsyncWebClient):
        self.client = client
        # Replace the standard MessageHandler with the NLMessageHandler for natural language support
        self.message_handler = NLMessageHandler(client)
        self.file_handler = SlackFileHandler(client)
        LoggerSetup.setup_logging()  # Call the logging setup method
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("EventHandler initialized with NLMessageHandler for natural language processing")

    async def handle_event(self, event):
        self.logger.info(f"Handling event: {event.get('type')}")

        # Ignore messages sent by the bot itself
        if 'bot_id' in event or event.get('subtype') == 'bot_message':
            self.logger.info("Ignoring bot message")
            return

        event_type = event.get('type')
        try:
            if event_type == 'message':
                await self.message_handler.handle(event)
            elif event_type == 'file_shared':
                await self.file_handler.handle(event)
            else:
                self.logger.warning(f"Unhandled event type: {event_type}")
        except Exception as e:
            self.logger.error(f"Error handling {event_type} event: {str(e)}", exc_info=True)
