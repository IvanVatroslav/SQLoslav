# slack_bot/logger.py

import logging


class LoggerSetup:
    @staticmethod
    def setup_logging():
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s')

        # Suppress DEBUG logs from slack_sdk
        logging.getLogger("slack_sdk").setLevel(logging.INFO)
