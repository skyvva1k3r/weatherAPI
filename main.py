import redis
import requests
import json
from dotenv import load_dotenv
import os
import time
from operator import itemgetter
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import subprocess
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Главная страница - отдаем HTML"""
    try:
        return send_file('index.html')
    except:
        return jsonify({"message": "Weather API is running. Use /weather endpoint"}), 200

API_KEY = os.getenv("API_KEY")


r = redis.Redis(host='localhost', port=6379, decode_responses=True)
key = f"{API_KEY}"

@app.route('/weather')
def weather():
    city = request.args.get('city')
    days = request.args.get('days', 7)
    if city is None:
        return jsonify({"error": "City parameter is required"}), 400
    try :
        days = int(days)
    except ValueError:
        return jsonify({"error": "Days parameter must be an integer"}), 400
    if days > 15:
        return jsonify({"error": "Days parameter must be less than 14"}), 400
    if days < 1:
        return jsonify({"error": "Days parameter must be greater than 0"}), 400

    result = get_data(city.lower(), days)
    if "error" in result: 
        return jsonify(result), 404
    return jsonify(result), 200

def get_data(city, days):
        cur = f"{time.strftime('%Y-%m-%d', time.localtime())}"
        req = ["tempmax", "tempmin", "feelslike", "pressure", "windspeed", "visibility", "datetime", "icon",
               "conditions", "humidity", "precip", "precipprob", "uvindex"]
        res = []
        print(r.ping())
        
        if r.exists(f"{city}_{cur}") == 0 :
            print("No data in Redis, fetching...")
            response = requests.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={key}")
            if response.status_code != 200:
                return {"error": "City not found"}
            r.set(f"{city}_{cur}", json.dumps(response.json()))
        else: 
            print("Data in Redis, fetching...")
        load = json.loads(r.get(f"{city}_{cur}"))["days"]
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)