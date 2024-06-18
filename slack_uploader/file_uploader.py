import requests
import logging
import os


class FileUploader:
    def upload_file_content(self, upload_url: str, file_path: str):
        logging.info(f"Uploading file content to URL: {upload_url}")
        filesize = os.path.getsize(file_path)
        with open(file_path, 'rb') as file_content:
            response = requests.put(
                url=upload_url,
                headers={
                    'Content-Type': 'application/octet-stream; charset=utf-8',
                    'Content-Length': str(filesize)  # Adding the Content-Length header
                },
                data=file_content
            )
        logging.info(f"Response from file upload (upload_file_content): {response.status_code}")
        response.raise_for_status()
        logging.info(f"File content uploaded successfully to: {upload_url}")
