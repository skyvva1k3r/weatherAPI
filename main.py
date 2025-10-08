import redis
import requests
import json
from dotenv import load_dotenv
import os
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
time = 0

def get_data(city, time, key):
        if r.exists(f"{city}_{time}") == 0:
            print("No data in Redis, fetching...")
            r.set(f"{city}_{time}", json.dumps(requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={city}&days={time}&aqi=no&alerts=no").json()))
        else: 
            print("Data in Redis, fetching...")

get_data(city, time, key)
