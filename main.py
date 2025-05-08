from fastapi import FastAPI, Request
import uvicorn
from slack_bot import SlackBot
import logging
import os
from dotenv import load_dotenv
from config.mistral_config import has_valid_api_key

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("sqloslav")

# Load environment variables
load_dotenv()

app = FastAPI(title="SQLoslav API", description="A Slack bot for SQL queries")
slack_bot = SlackBot()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "SQLoslav is running"}


@app.post("/slack/events")
async def slack_events(request: Request):
    data = await request.json()
    logger.info(f"Received event: {data}")
    # Add more detailed logging
    logger.info(f"Event type: {data.get('type')}")
    if 'event' in data:
        logger.info(f"Inner event type: {data.get('event', {}).get('type')}")
        logger.info(f"User: {data.get('event', {}).get('user')}")
        logger.info(f"Text: {data.get('event', {}).get('text')}")

    response = await slack_bot.handle_event(data)
    logger.info(f"Response: {response}")
    return response


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    logger.info(f"Starting SQLoslav on port {port}")
    
    # Log important environment variables for debugging
    logger.info(f"Environment variables check:")
    logger.info(f"SLACK_BOT_TOKEN present: {bool(os.getenv('SLACK_BOT_TOKEN'))}")
    logger.info(f"MISTRAL_API_KEY valid: {has_valid_api_key()}")
    logger.info(f"Data directory: {os.getenv('DATA_DIR', '/app/data')}")
    logger.info(f"Download directory: {os.getenv('DOWNLOAD_DIR', '/app/downloads')}")

    uvicorn.run(app, host="0.0.0.0", port=port)
