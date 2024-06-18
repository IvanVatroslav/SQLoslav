import requests
import logging
import os


class UploadCompleter:
    def __init__(self, token: str):
        self.token = token

    def complete_upload(self, file_id: str, file_path: str, channel_id: str):
        logging.info(f"Completing file upload for File ID: {file_id}, Channel ID: {channel_id}")
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        data = {
            'files': [{'id': file_id, 'title': os.path.basename(file_path)}],
            'channel_id': channel_id
        }
        response = requests.post(
            url='https://slack.com/api/files.completeUploadExternal',
            headers=headers,
            json=data
        )
        logging.info(f"Response from Slack (complete_upload): {response.text}")
        response.raise_for_status()
        response_json = response.json()
        if response_json.get('ok'):
            file_url = response_json['files'][0]['permalink']
            logging.info(f"File upload completed successfully: {file_url}")
            return file_url
        else:
            error_message = response_json.get('error', 'Unknown error')
            logging.error(f"Failed to complete file upload: {error_message}")
            raise Exception(f"Failed to complete file upload: {error_message}")
