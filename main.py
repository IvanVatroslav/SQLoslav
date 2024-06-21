from fastapi import FastAPI, Request
import uvicorn
from slack_bot import SlackBot
import logging

app = FastAPI()
slack_bot = SlackBot()


@app.post("/slack/events")
async def slack_events(request: Request):
    data = await request.json()
    logging.info(f"Received event: {data}")
    response = await slack_bot.handle_event(data)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
