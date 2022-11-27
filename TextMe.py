from twilio.rest import Client
from dotenv import load_dotenv
import os
from TalkToWeatherAPI import TalkToWeatherAPI

load_dotenv()


class TextMe:
    def __init__(self):
        self.account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        self.auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, message: str, send_to: str):
        message = self.client.messages.create(
            body=message, from_="+15618165335", to=send_to
        )


class TextTheForecast(TextMe):
    def __init__(self, send_to):
        super().__init__()
        self.send_to = send_to
        self.message = ""

    def text_if_snow(self):
        message = "It's going to snow in the next 24 hours"
        api = TalkToWeatherAPI()
        data = api.one_day_snowfall_forecast()
        self.evaluate_data(data, message)

    def send_forecast(self, message: str, send_to: str):
        message = self.client.messages.create(
            body=message, from_="+15618165335", to=send_to
        )

    def evaluate_data(self, data, message):
        for i in data:
            if i > 0:
                self.message = message
                self.send_forecast(self.message, self.send_to)
                break


t = TextTheForecast("+14358300726")
t.text_if_snow()
