
from flask import Flask, request, jsonify
import joblib
import numpy as np
from datetime import datetime
import logging

app = Flask(__name__)
model = joblib.load("iris_model.pkl")

LOG_FILE = "/var/log/ml_api.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(message)s"
)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "features" not in data:
        return jsonify({"error": "Provide features"}), 400

    features = np.array(data["features"], dtype=float).reshape(1, -1)

    if features.shape[1] != 4:
        return jsonify({"error": "Provide exactly 4 features"}), 400

    prediction = model.predict(features)[0]

    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "input": data["features"],
        "prediction": str(prediction)
    }
    logging.info(log)

    return jsonify({"prediction": str(prediction)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
