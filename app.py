from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Load regions.json
json_path = os.path.join(os.path.dirname(__file__), "regions.json")
with open(json_path, "r") as f:
    body_regions = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detect_region", methods=["POST"])
def detect_region():
    data = request.get_json()
    x, y, z = data.get("x"), data.get("y"), data.get("z")

    detected_region = "Unknown"

    for region, (y_min, y_max) in body_regions.items():
        if y_min <= y <= y_max:
            detected_region = region

            # Refinement rules
            if region == "Chest":
                if -0.1 <= x <= 0.1 and 0.62 <= y <= 0.66:
                    detected_region = "Heart"
                elif x > 0.1:
                    detected_region = "Right Lung"
                elif x < -0.1:
                    detected_region = "Left Lung"

            elif region == "Stomach":
                if x > 0.1:
                    detected_region = "Liver"
                elif x < -0.1:
                    detected_region = "Spleen"

            elif region == "Pelvis":
                if -0.05 <= x <= 0.05:
                    detected_region = "Bladder"

            break

    return jsonify({"region": detected_region})

if __name__ == "__main__":
    app.run(debug=True)
