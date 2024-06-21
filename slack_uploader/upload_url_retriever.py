import requests
import logging
import os


class UploadURLRetriever:
    def __init__(self, token: str):
        self.token = token

    def get_upload_url(self, file_path: str, channel_id: str):
        logging.info("Requesting upload URL from Slack")
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/x-www-form-urlencoded;'
        }
        filename = os.path.basename(file_path)
        filesize = os.path.getsize(file_path)
        logging.info(f"Filename: {filename}, Filesize: {filesize}")

        data = {
            'filename': filename,
            'length': filesize,
            'channels': channel_id,
            'alt_txt': 'File uploaded by bot',
            'snippet_type': 'csv',
            'filetype': 'csv',
            'mime_type': 'text/csv'
        }

        logging.info(f"Payload for get_upload_url: {data}")
        response = requests.post(
            url='https://slack.com/api/files.getUploadURLExternal',
            headers=headers,
            data=data  # Use `data` instead of `json` for x-www-form-urlencoded
        )
        logging.info(f"Response from Slack (get_upload_url): {response.text}")
        response.raise_for_status()
        response_json = response.json()
        if response_json.get('ok'):
            upload_url = response_json['upload_url']
            file_id = response_json['file_id']
            logging.info(f"Received upload URL: {upload_url}, File ID: {file_id}")
            return upload_url, file_id
        else:
            error_message = response_json.get('error', 'Unknown error')
            logging.error(f"Failed to get upload URL from Slack: {error_message}")
            raise Exception(f"Failed to get upload URL from Slack: {error_message}")
