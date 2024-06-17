from fastapi import FastAPI, Request
import uvicorn
from slack_bot import SlackBot
import logging

app = FastAPI()
slack_bot = SlackBot()


@app.post("/slack/events")
async def slack_events(request: Request):
    data = await request.json()
    channel_id = data.get('event', {}).get('channel')
    logging.info(f"Received event for channel: {channel_id}")
    return await slack_bot.handle_event(request, channel_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
