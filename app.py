from flask import Flask, jsonify, render_template, request
import random
from geopy.distance import geodesic
import os

app = Flask(__name__)

# Coordenadas aproximadas del área de Temuco
TEMUCO_BOUNDS = {
    "north": -38.7095,
    "south": -38.7620,
    "east": -72.5896,
    "west": -72.6702
}

def generate_random_location():
    """Genera una ubicación aleatoria dentro de Temuco."""
    lat = random.uniform(TEMUCO_BOUNDS["south"], TEMUCO_BOUNDS["north"])
    lon = random.uniform(TEMUCO_BOUNDS["west"], TEMUCO_BOUNDS["east"])
    return {"latitude": lat, "longitude": lon}

@app.route("/")
def home():
    return render_template("street_view.html")

@app.route("/random-location")
def random_location():
    location = generate_random_location()
    return jsonify(location)

@app.route("/check-location", methods=["POST"])
def check_location():
    data = request.json
    actual = (data["actual"]["latitude"], data["actual"]["longitude"])
    guess = (data["guess"]["latitude"], data["guess"]["longitude"])
    distance = geodesic(actual, guess).meters
    return jsonify({"distance": distance})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)