import redis
import requests
import json
from dotenv import load_dotenv
import os
import time

load_dotenv()

API_KEY = os.getenv("API_KEY")

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
key = f"{API_KEY}"

def get_data(city, days):
        cur = f"{time.strftime('%Y-%m-%d', time.localtime())}"
        req = ["tempmax", "tempmin", "feelslike", "pressure", "windspeed", "visibility", "datetime", "icon",
               "conditions", "humidity", "precip", "precipprob", "uvindex"]
        res = []
        online = None
        try:
            r.ping()
            online = True
        except redis.ConnectionError:
            online = False
        if online:
            if r.exists(f"{city}_{cur}") == 0:
                print("No data in Redis, fetching...")
                response = requests.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={key}")
                if response.status_code != 200:
                    return {"error": "City not found"}
                r.set(f"{city}_{cur}", json.dumps(response.json()))
            else: 
                print("Data in Redis, fetching...")
            load = json.loads(r.get(f"{city}_{cur}"))
        else:
            load = requests.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={key}").json()
        load = load["days"]
        for i in range(days):
            temp = dict()
            for j in req:
                temp.update({j : load[i][j]})
                if j == "tempmax" or j == "tempmin" or j == "feelslike":
                    temp[j] = round(((temp[j] -32)*5)/9, 1)
            res.append(temp)
        return {"status" : "success", 
                "city" : city, 
                "days" : days,
                "data" : res}