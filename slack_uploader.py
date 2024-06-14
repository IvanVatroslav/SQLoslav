import requests
import logging


class SlackUploader:
    def __init__(self, channel: str, token: str):
        self.channel = channel
        self.token = token

    def upload_file_to_slack(self, file_path: str) -> str:
        logging.info(f"Uploading file to Slack: {file_path}")
        try:
            with open(file_path, 'rb') as file_content:
                response = requests.post(
                    url='https://slack.com/api/files.upload',
                    headers={'Authorization': f'Bearer {self.token}'},
                    files={'file': file_content},
                    data={'channels': self.channel}
                )
            response.raise_for_status()

            response_json = response.json()
            if response_json.get('ok'):
                file_url = response_json['file']['permalink']
                logging.info(f"File uploaded successfully: {file_url}")
                return file_url
            else:
                error_message = response_json.get('error', 'Unknown error')
                logging.error(f"Failed to upload file to Slack: {error_message}")
                raise Exception(f"Failed to upload file to Slack: {error_message}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request to Slack API failed: {e}")
            raise

    def prepare_slack_payload(self, markdown_table: str) -> str:
        logging.info("Preparing Slack payload")
        return f"```\n{markdown_table}\n```"
