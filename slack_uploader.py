import requests
import logging
import os


class SlackUploader:
    def __init__(self, token: str):
        self.token = token

    def get_upload_url(self, file_path: str):
        logging.info("Requesting upload URL from Slack")
        headers = {
            'Authorization': f'Bearer ' + self.token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        filename = os.path.basename(file_path)
        filesize = os.path.getsize(file_path)
        logging.info(f"Filename: {filename}, Filesize: {filesize}")

        data = {
            'filename': filename,
            'length': filesize
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

    def upload_file_content(self, upload_url: str, file_path: str):
        logging.info(f"Uploading file content to URL: {upload_url}")
        filesize = os.path.getsize(file_path)
        with open(file_path, 'rb') as file_content:
            response = requests.put(
                url=upload_url,
                headers={
                    'Content-Type': 'application/octet-stream',
                    'Content-Length': str(filesize)  # Adding the Content-Length header
                },
                data=file_content
            )
        logging.info(f"Response from file upload (upload_file_content): {response.status_code}")
        response.raise_for_status()
        logging.info(f"File content uploaded successfully to: {upload_url}")

    def complete_upload(self, file_id: str, file_path: str, channel_id: str):
        logging.info(f"Completing file upload for File ID: {file_id}, Channel ID: {channel_id}")
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        data = {
            'files': [{'id': file_id}],
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

    def upload_file_to_slack(self, file_path: str, channel_id: str):
        logging.info(f"Uploading file to Slack: {file_path} to channel: {channel_id}")
        try:
            upload_url, file_id = self.get_upload_url(file_path)
            self.upload_file_content(upload_url, file_path)
            return self.complete_upload(file_id, file_path, channel_id)
        except Exception as e:
            logging.error(f"Error uploading file: {e}")
            raise
