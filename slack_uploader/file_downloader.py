import requests
import logging
import os
from requests.exceptions import RequestException


class FileDownloader:
    def __init__(self, token: str):
        self.token = token
        logging.getLogger().setLevel(logging.DEBUG)

    def download_file(self, file_url: str, filename: str) -> str:
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            logging.info(f"Attempting to download file from URL: {file_url}")
            response = requests.get(file_url, headers=headers)
            response.raise_for_status()

            logging.debug(f"Response headers: {response.headers}")
            logging.debug(f"Response status code: {response.status_code}")

            content_type = response.headers.get('Content-Type', 'Unknown')
            content_length = response.headers.get('Content-Length', 'Unknown')
            logging.info(f"File Content-Type: {content_type}, Content-Length: {content_length}")

            file_path = os.path.join('C:\\Users\\ivan.zeljeznjak\\Desktop\\slack_downloads', filename)

            with open(file_path, 'wb') as f:
                f.write(response.content)

            logging.info(f"File downloaded successfully: {file_path}")
            logging.debug(f"File size: {os.path.getsize(file_path)} bytes")

            # Log the first few bytes of the file content
            with open(file_path, 'rb') as f:
                content_preview = f.read(100)
            logging.debug(f"File content preview (first 100 bytes): {content_preview}")

            return file_path

        except RequestException as e:
            logging.error(f"Error downloading file: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Response status code: {e.response.status_code}")
                logging.error(f"Response content: {e.response.content}")
            raise
        except IOError as e:
            logging.error(f"Error writing file: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            raise

    def test_connection(self, test_url: str = "https://slack.com/api/api.test"):
        try:
            response = requests.get(test_url, headers={'Authorization': f'Bearer {self.token}'})
            response.raise_for_status()
            logging.info(f"Connection test successful. Response: {response.json()}")
        except Exception as e:
            logging.error(f"Connection test failed: {str(e)}")
