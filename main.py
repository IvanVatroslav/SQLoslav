from fastapi import FastAPI, Request
import uvicorn
from slack_bot import SlackBot

app = FastAPI()
slack_bot = SlackBot()


@app.post("/slack/events")
async def slack_events(request: Request):
    return await slack_bot.handle_event(request)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
