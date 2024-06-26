# slack_bot/slack_file_handler.py

import logging
import os
import aiohttp
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError


class SlackFileHandler:
    def __init__(self, client: AsyncWebClient):
        self.client = client
        logging.getLogger().setLevel(logging.DEBUG)

    async def handle(self, event):
        file_id = event.get('file_id')
        channel_id = event.get('channel_id')
        logging.info(f"File shared event received. File ID: {file_id}, Channel ID: {channel_id}")

        try:
            file_info = await self.get_file_info(file_id)
            await self.log_file_details(file_info)

            if self.is_file_type_supported(file_info):
                download_path = await self.download_file(file_info)
                await self.process_file(download_path, channel_id)
            else:
                await self.send_unsupported_file_message(channel_id, file_info['name'])

        except Exception as e:
            logging.error(f"Error handling file_shared event: {str(e)}", exc_info=True)
            await self.send_error_message(channel_id, str(e))

    async def get_file_info(self, file_id):
        try:
            response = await self.client.files_info(file=file_id)
            return response['file']
        except SlackApiError as e:
            logging.error(f"Error getting file info: {str(e)}", exc_info=True)
            raise

    async def log_file_details(self, file_info):
        logging.info(f"File Details:")
        logging.info(f"  Name: {file_info.get('name')}")
        logging.info(f"  Type: {file_info.get('filetype')}")
        logging.info(f"  Size: {file_info.get('size')} bytes")
        logging.info(f"  Created: {file_info.get('created')}")
        logging.info(f"  URL Private: {file_info.get('url_private')}")
        logging.info(f"  URL Private Download: {file_info.get('url_private_download')}")

    def is_file_type_supported(self, file_info):
        supported_types = ['csv', 'xls', 'xlsx', 'txt']  # Add or remove types as needed
        return file_info.get('filetype', '').lower() in supported_types

    async def download_file(self, file_info):
        url = file_info['url_private_download']
        filename = file_info['name']
        headers = {"Authorization": f"Bearer {self.client.token}"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
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
                    await self.verify_download(download_path, file_info['size'])
                    return download_path
                else:
                    logging.error(f"Failed to download file. Status: {resp.status}")
                    raise Exception(f"File download failed with status {resp.status}")

    async def verify_download(self, file_path, expected_size):
        actual_size = os.path.getsize(file_path)
        if actual_size != expected_size:
            logging.warning(f"Downloaded file size ({actual_size}) does not match expected size ({expected_size})")
        else:
            logging.info("Downloaded file size verified successfully")

    async def process_file(self, file_path, channel_id):
        # Implement your file processing logic here
        # For example, you might want to read the file, perform some analysis, etc.
        logging.info(f"Processing file: {file_path}")
        # Comment out or remove the following lines to stop sending the processing message
        # await self.client.chat_postMessage(
        #     channel=channel_id,
        #     text=f"File {os.path.basename(file_path)} has been processed successfully."
        # )

    async def send_unsupported_file_message(self, channel_id, filename):
        await self.client.chat_postMessage(
            channel=channel_id,
            text=f"Sorry, the file type of {filename} is not supported for processing."
        )

    async def send_error_message(self, channel_id, error_message):
        await self.client.chat_postMessage(
            channel=channel_id,
            text=f"An error occurred while processing the shared file: {error_message}"
        )
