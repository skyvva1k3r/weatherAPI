from flask import jsonify, send_file, request
from services import get_data
from __main__ import app

@app.route('/')
def index():
    try:
        return send_file('weather-app(AI gen.).html')
    except:
        return jsonify({"message": "Weather API is running. Use /weather endpoint"}), 200
    
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