import logging
from slack_sdk import WebClient
from slack_uploader.slack_uploader import SlackUploader


class SlackFileHandler:
    def __init__(self, client: WebClient):
        self.client = client
        self.uploader = SlackUploader(token=client.token)

    async def handle(self, event):
        file_id = event.get('file_id')
        channel_id = event.get('channel_id')
        logging.info(f"File shared event received. File ID: {file_id}, Channel ID: {channel_id}")

        try:
            response = self.client.files_info(file=file_id)
            file_info = response['file']
            file_url = file_info['url_private']
            filename = file_info['name']
            logging.info(f"File URL: {file_url}")

            file_path = self.uploader.download_file(file_url, filename)
            uploaded_file_url = self.uploader.upload_file_to_slack(file_path, channel_id)
            logging.info(f"File re-uploaded successfully: {uploaded_file_url}")

            self.client.chat_postMessage(channel=channel_id, text=f"File re-uploaded successfully: {uploaded_file_url}")
        except Exception as e:
            logging.error(f"Error handling file_shared event: {e}")
