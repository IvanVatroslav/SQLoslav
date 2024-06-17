import logging


class ErrorHandler:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def handle_error(self, error: Exception, context: str = "") -> str:
        error_message = f"Error in {context}: {str(error)}"
        logging.error(error_message)
        return error_message
