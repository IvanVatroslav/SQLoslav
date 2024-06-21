import os
import logging
from slack_sdk.web.async_client import AsyncWebClient
import aiohttp


class SlackUploader:
    def __init__(self, token: str):
        self.client = AsyncWebClient(token=token)

    async def upload_file_to_slack(self, file_path: str, channel_id: str) -> str:
        logging.info(f"Uploading file to Slack: {file_path} to channel: {channel_id}")
        try:
            with open(file_path, 'rb') as file_content:
                response = await self.client.files_upload_v2(
                    channel=channel_id,
                    file=file_content,
                    filename=os.path.basename(file_path),
                    initial_comment="Here's the query result file."
                )
            file_url = response['file']['permalink']
            logging.info(f"File uploaded successfully. URL: {file_url}")
            return file_url
        except Exception as e:
            logging.error(f"Error uploading file: {str(e)}")
            raise

    async def download_file(self, file_url: str, filename: str) -> str:
        logging.info(f"Downloading file from Slack: {file_url}")
        headers = {"Authorization": f"Bearer {self.client.token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url, headers=headers) as resp:
                if resp.status == 200:
                    download_path = os.path.join('downloads', filename)
                    os.makedirs('downloads', exist_ok=True)
                    with open(download_path, 'wb') as f:
                        while True:
                            chunk = await resp.content.read(8192)
                            if not chunk:
                                break
                            f.write(chunk)
                    logging.info(f"File downloaded successfully: {download_path}")
                    return download_path
                else:
                    logging.error(f"Failed to download file. Status: {resp.status}")
                    raise Exception(f"File download failed with status {resp.status}")
