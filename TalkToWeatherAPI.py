# pip install tzinfo to populate timezone dict if your OS does not have one
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests
from UnitConverter import UnitConverter


class TalkToWeatherAPI:
    def __init__(self, timezone: str = "America/Denver"):
        todays_date = datetime.now(ZoneInfo("America/Denver")).strftime("%Y-%m-%d")
        tomorrows_date = (
            datetime.now(ZoneInfo("America/Denver")) + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        self.timezone = timezone
        self.start_date = todays_date
        self.end_date = tomorrows_date
        self.latitude = 40.36
        self.longitude = -111.74
        # self.hourly = "temperature_2m,precipitation,rain,showers,snowfall"
        self.hourly = ["precipitation", "rain", "showers", "snowfall"]

        self.params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timezone": self.timezone,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "hourly": self.hourly,
        }

    def __str__(self):
        return f"Class for pulling in the next 24 hours forecast. Your timezone is {self.timezone}"

    def compare_values(self, dataset: list, cm_or_mm: str):
        l = 0
        if cm_or_mm.lower() == "mm":
            for data in dataset:
                uc = UnitConverter(data)
                dataset[l] = uc.mm_to_inches()
                l += 1
            return dataset
        elif cm_or_mm.lower() == "cm":
            for data in dataset:
                uc = UnitConverter(data)
                dataset[l] = uc.cm_to_inches()
                l += 1
            return dataset
        else:
            raise ValueError('Parameter cm_or_mm needs to be either "cm" or "mm".')

    def one_day_snowfall_forecast(self):
        request_url = "https://api.open-meteo.com/v1/forecast"
        request = requests.get(request_url, params=self.params)
        request_payload = request.json()
        # return request_payload
        now_time = datetime.now(ZoneInfo(self.timezone)).strftime("%Y-%m-%dT%H:00")
        i = 0
        for hour in request_payload["hourly"]["time"]:
            # print(f"hour is: {hour}")
            if hour == now_time:
                data = request_payload["hourly"]["snowfall"][i : i + 25]
                data = self.compare_values(dataset=data, cm_or_mm="cm")
                return data
            i += 1

    def one_day_precipitation_forecast(self):
        request_url = "https://api.open-meteo.com/v1/forecast"
        request = requests.get(request_url, params=self.params)
        request_payload = request.json()
        # return request_payload
        now_time = datetime.now(ZoneInfo(self.timezone)).strftime("%Y-%m-%dT%H:00")
        i = 0
        for hour in request_payload["hourly"]["time"]:
            # print(f"hour is: {hour}")
            if hour == now_time:
                data = request_payload["hourly"]["snowfall"][i : i + 25]
                data = self.compare_values(dataset=data, cm_or_mm="mm")
                return data
            i += 1
