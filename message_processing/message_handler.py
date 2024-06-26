# message_processing/message_handler.py

import logging
from slack_sdk.web.async_client import AsyncWebClient
from message_processing.message_processor import MessageProcessor


class MessageHandler:
    def __init__(self, client: AsyncWebClient):
        self.client = client
        self.processor = MessageProcessor()
        logging.getLogger().setLevel(logging.INFO)

    async def handle(self, event):
        message = event.get('text', '')
        channel_id = event.get('channel')
        user = event.get('user')
        thread_ts = event.get('thread_ts')

        logging.info(f"Handling message from user {user} in channel {channel_id}")

        try:
            response_message = await self.processor.process_message(message, channel_id)

            # Comment out or remove the following block to stop sending the response message
            # if not response_message:
            #     response_message = "Query executed successfully, but no data was returned."
            #
            # await self.client.chat_postMessage(
            #     channel=channel_id,
            #     text=response_message,
            #     thread_ts=thread_ts
            # )

            logging.info(f"Response processed for channel {channel_id}")

        except Exception as e:
            error_message = f"An error occurred while processing your message: {str(e)}"
            logging.error(f"Error processing message: {str(e)}", exc_info=True)

            await self.client.chat_postMessage(
                channel=channel_id,
                text=error_message,
                thread_ts=thread_ts if thread_ts else None
            )
