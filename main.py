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
    # Add more detailed logging
    logging.info(f"Event type: {data.get('type')}")
    if 'event' in data:
        logging.info(f"Inner event type: {data.get('event', {}).get('type')}")
        logging.info(f"User: {data.get('event', {}).get('user')}")
        logging.info(f"Text: {data.get('event', {}).get('text')}")

    response = await slack_bot.handle_event(data)
    logging.info(f"Response: {response}")
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
