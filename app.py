from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('weather.html')


# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)  # Allow frontend to call backend locally

# 🧩 Function to fetch and parse weather data from wttr.in
import re

def scrape_weather(city):
    url = f"https://wttr.in/{city}?format=%C+%t+%w+%h+%v+%f"
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        text = response.text.strip()

        if "Unknown location" in text or "Sorry" in text:
            return {"error": f"City '{city}' not found."}

        # Use regex to extract values
        temp_match = re.search(r'([+-]?\d+°C)', text)
        condition_match = re.match(r'^[^\s]+', text)
        wind_match = re.search(r'(\d+ km/h)', text)
        humidity_match = re.search(r'(\d+%)', text)
        visibility_match = re.search(r'(\d+ km)', text)
        feels_match = re.search(r'Feels like ([+-]?\d+°C)', text)

        return {
            "city": city.title(),
            "condition": condition_match.group(0) if condition_match else "N/A",
            "temperature": temp_match.group(1) if temp_match else "N/A",
            "windspeed": wind_match.group(1) if wind_match else "N/A",
            "humidity": humidity_match.group(1) if humidity_match else "N/A",
            "visibility": visibility_match.group(1) if visibility_match else "N/A",
            "feelslike": feels_match.group(1) if feels_match else "N/A",
            "airquality": "N/A"
        }

    except Exception as e:
        return {"error": str(e)}





# 🌤 Weather API route
@app.route('/weather')
def weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'No city provided'}), 400

    data = scrape_weather(city)
    if 'error' in data:
        return jsonify(data), 500

    return jsonify(data)


# 🏠 Serve frontend file correctly
@app.route('/')
def home():
    # Serves the weather.html inside /static folder
    return send_from_directory(app.static_folder, 'weather.html')


# 🚀 Run the Flask app
if __name__ == '__main__':
    # Run on all local interfaces so it’s visible at 127.0.0.1 and localhost
    app.run(host='0.0.0.0', port=5000, debug=True)

