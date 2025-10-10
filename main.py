import redis
import requests
import json
from dotenv import load_dotenv
import os
import time
from operator import itemgetter
from flask import Flask, jsonify, request
import subprocess
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

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
key = f"{API_KEY}"

@app.route('/weather')
def weather():
    city = request.args.get('city')
    return jsonify(get_data(city))

def get_data(city):
        cur = f"{time.strftime('%Y-%m-%d', time.localtime())}"
        req = ["tempmax", "tempmin", "feelslike", "pressure", "windspeed", "visibility"]
        res = []
        if r.exists(f"{city}_{cur}") == 0:
            print("No data in Redis, fetching...")
            r.set(f"{city}_{cur}", json.dumps(requests.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={key}").json()))
        else: 
            print("Data in Redis, fetching...")
        for i in range(14):
            res.append(itemgetter(*req)(json.loads(r.get(f"{city}_{cur}"))["days"][i]))
            res[i] = list(res[i])
            res[i][0] = round(((res[i][0] -32)*5)/9, 1)
            res[i][1] = round(((res[i][1] -32)*5)/9, 1)
            res[i][2] = round(((res[i][2] -32)*5)/9, 1)
            res[i] = tuple(res[i])
        return res


if __name__ == '__main__':
    app.run()