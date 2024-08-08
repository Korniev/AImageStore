import json
import os

from channels.generic.websocket import AsyncWebsocketConsumer
import openai

openai.api_key = ''
OPENAPI_KEY = os.getenv("OPENAPI_KEY")


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        response = openai.Completion.create(
            model="davinci",
            prompt=message,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )

        response_message = response.choices[0].text.strip()

        await self.send(text_data=json.dumps({
            'message': response_message
        }))
