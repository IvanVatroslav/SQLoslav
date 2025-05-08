import logging
from slack_sdk.web.async_client import AsyncWebClient
from message_processing.nl_message_processor import NLMessageProcessor


class NLMessageHandler:
    """
    Handles messages with natural language processing capabilities.
    This extends the functionality of the standard MessageHandler
    by using the NLMessageProcessor which can handle both SQL and natural language queries.
    """
    
    def __init__(self, client: AsyncWebClient):
        """
        Initialize the NLMessageHandler with a Slack client.
        
        Args:
            client: The Slack AsyncWebClient to use for sending messages.
        """
        self.client = client
        self.processor = NLMessageProcessor()
        logging.getLogger().setLevel(logging.INFO)
        logging.info("NLMessageHandler initialized with natural language processing capabilities")

    async def handle(self, event):
        """
        Handle a Slack message event.
        
        Args:
            event: The Slack event containing the message.
        """
        message = event.get('text', '')
        channel_id = event.get('channel')
        user = event.get('user')
        thread_ts = event.get('thread_ts')

        logging.info(f"Handling message with NL capability from user {user} in channel {channel_id}")

        try:
            response_message = await self.processor.process_message(message, channel_id)

            if response_message:  # Only send a message if there's a response
                await self.client.chat_postMessage(
                    channel=channel_id,
                    text=response_message,
                    thread_ts=thread_ts
                )

            logging.info(f"Response processed for channel {channel_id}")

        except Exception as e:
            error_message = f"An error occurred while processing your message: {str(e)}"
            logging.error(f"Error processing message: {str(e)}", exc_info=True)

            await self.client.chat_postMessage(
                channel=channel_id,
                text=error_message,
                thread_ts=thread_ts if thread_ts else None
            ) 