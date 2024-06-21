import logging


class ErrorHandler:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    @staticmethod
    def handle_error(error: Exception, context: str = "", channel_id: str = "") -> str:
        error_message = f"Error in {context} for channel {channel_id}: {str(error)}"
        logging.error(error_message)
        return error_message
