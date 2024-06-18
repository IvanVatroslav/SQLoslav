import logging
from slack_uploader.upload_url_retriever import UploadURLRetriever
from slack_uploader.file_uploader import FileUploader
from slack_uploader.upload_completer import UploadCompleter
from slack_uploader.file_downloader import FileDownloader


class SlackUploader:
    def __init__(self, token: str):
        self.url_retriever = UploadURLRetriever(token)
        self.file_uploader = FileUploader()
        self.upload_completer = UploadCompleter(token)
        self.file_downloader = FileDownloader(token)

    def upload_file_to_slack(self, file_path: str, channel_id: str):
        logging.info(f"Uploading file to Slack: {file_path} to channel: {channel_id}")
        try:
            upload_url, file_id = self.url_retriever.get_upload_url(file_path, channel_id)
            self.file_uploader.upload_file_content(upload_url, file_path)
            file_url = self.upload_completer.complete_upload(file_id, file_path, channel_id)
            return file_url  # Using permalink to ensure preview
        except Exception as e:
            logging.error(f"Error uploading file: {e}")
            raise

    def download_file(self, file_url: str, filename: str) -> str:
        return self.file_downloader.download_file(file_url, filename)
