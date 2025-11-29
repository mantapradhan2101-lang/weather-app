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
import requests

def scrape_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()

        # Current condition
        current = data['current_condition'][0]

        return {
            "city": city.title(),
            "condition": current.get('weatherDesc', [{}])[0].get('value', 'N/A'),
            "temperature": current.get('temp_C', 'N/A') + "°C",
            "windspeed": current.get('windspeedKmph', 'N/A') + " km/h",
            "humidity": current.get('humidity', 'N/A') + "%",
            "visibility": current.get('visibility', 'N/A') + " km",
            "feelslike": current.get('FeelsLikeC', 'N/A') + "°C",
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


