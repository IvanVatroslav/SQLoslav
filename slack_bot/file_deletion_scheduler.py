import os
import logging
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class FileDeletionScheduler:
    def __init__(self, slack_token):
        self.client = WebClient(token=slack_token)
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def delete_file(self, file_id):
        try:
            response = self.client.files_delete(file=file_id)
            if response["ok"]:
                logging.info(f"File {file_id} deleted successfully.")
            else:
                logging.error(f"Failed to delete file {file_id}: {response['error']}")
        except SlackApiError as e:
            logging.error(f"Slack API error: {e.response['error']}")

    def schedule_file_deletion(self, file_id, delay_seconds):
        # Schedule the deletion
        run_date = datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds)
        self.scheduler.add_job(self.delete_file, 'date', run_date=run_date, args=[file_id])
        logging.info(f"File {file_id} scheduled for deletion in {delay_seconds} seconds.")
