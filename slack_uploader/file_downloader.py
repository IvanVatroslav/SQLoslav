import requests
import logging
import os


class FileDownloader:
    def __init__(self, token: str):
        self.token = token

    def download_file(self, file_url: str, filename: str) -> str:
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(file_url, headers=headers)
        response.raise_for_status()
        file_path = os.path.join('C:\\Users\\ivan.zeljeznjak\\Desktop\\slack_downloads', filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        logging.info(f"File downloaded successfully: {file_path}")
        return file_path
