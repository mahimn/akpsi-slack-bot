import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import string
from datetime import datetime, timedelta
import time

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

client.chat_postMessage(channel='#testing-ground', text="Hello! The latest version of the Mu Rho Bot is now live in this channel.")
# You can replace 'testing-ground' with any channel that you would prefer

message_counts = {}

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    if BOT_ID != user_id and text:
        if 'when' and 'induction' in text.lower():
            client.chat_postMessage(channel=channel_id, text="Our next Induction is Feb 14th, 2021.")
        elif 'when' and 'midcourt' in text.lower():
            client.chat_postMessage(channel=channel_id, text="Our next Mid-Court is March 13th, 2021.")
        elif ('court of honor' or 'coh') and 'when' in text.lower():
            client.chat_postMessage(channel=channel_id, text="Our next Court of Honor is April 18th, 2021.")

@ app.route('/test', methods=['POST'])
def test():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id, text=f"I got the command message")
    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True)