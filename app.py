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
def scrape_weather(city):
    import re
 
    url = f"https://wttr.in/{city}?format=%C+%t+%w+%h+%v+%f"
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        text = response.text.strip()

        if not text or "Unknown" in text or "Sorry" in text:
            return {"error": f"City '{city}' not found or unavailable."}

        # Extract data with flexible regex patterns
        condition = re.search(r'^[A-Za-z ]+', text)
        temperature = re.search(r'([+-]?\d+°C)', text)
        windspeed = re.search(r'([←→↑↓]?\s*\d+\s?km/h)', text)
        humidity = re.search(r'(\d+%)', text)
        visibility = re.search(r'(\d+\s?km)(?!/)', text)
        feelslike = re.findall(r'([+-]?\d+°C)', text)

        # Fallbacks
        feelslike_val = feelslike[-1] if len(feelslike) > 1 else feelslike[0] if feelslike else "N/A"

        return {
            "city": city.title(),
            "condition": condition.group(0).strip() if condition else "N/A",
            "temperature": temperature.group(1) if temperature else "N/A",
            "windspeed": windspeed.group(1).replace(" ", "") if windspeed else "N/A",
            "humidity": humidity.group(1) if humidity else "N/A",
            "visibility": visibility.group(1) if visibility else "N/A",
            "feelslike": feelslike_val,
            "airquality": "N/A"
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Parsing error: {str(e)}"}




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
