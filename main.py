import redis
import requests
import json
from dotenv import load_dotenv
import os
import time
load_dotenv()
API_KEY = os.getenv("API_KEY")



#  top_cities = [
#     "Vienna",
#     "Copenhagen",
#     "Zurich",
#     "Melbourne",
#     "Vancouver",
#     "Tokyo",
#     "Osaka",
#     "Toronto",
#     "Berlin",
#     "Amsterdam",
#     "Sydney",
#     "Stockholm",
#     "Munich",
#     "Singapore",
#     "Helsinki",
#     "Oslo",
#     "Calgary",
#     "Seoul",
#     "London",
# "Auckland"
# ]



r = redis.Redis(host='localhost', port=6379, decode_responses=True)
key = f"{API_KEY}"

city = "Moscow"
date = "2025-10-09"
cur = f"{time.strftime('%Y-%m-%d', time.localtime())}"


def get_data(city, date, cur, key):
        if r.exists(f"{city}_{date}_{cur}") == 0:
            print("No data in Redis, fetching...")
            r.set(f"{city}_{date}_{cur}", json.dumps(requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={city}&dt={date}&aqi=no&alerts=no").json()))
        else: 
            print("Data in Redis, fetching...")
        print(json.loads(r.get(f"{city}_{date}_{cur}"))["forecast"]["forecastday"][0]["day"]["maxtemp_c"])


get_data(city, date, cur, key)