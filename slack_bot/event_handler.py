import logging
from slack_sdk import WebClient
from slack_message_handler import SlackMessageHandler
from slack_file_handler import SlackFileHandler

class EventHandler:
    def __init__(self, client: WebClient):
        self.client = client
        self.message_handler = SlackMessageHandler(client)
        self.file_handler = SlackFileHandler(client)

    async def handle(self, event):
        event_type = event.get('type')

        if event_type == 'message':
            await self.message_handler.handle(event)
        elif event_type == 'file_shared':
            await self.file_handler.handle(event)
