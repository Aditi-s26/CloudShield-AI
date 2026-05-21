from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("model.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    duration = int(data["duration"])
    src_bytes = int(data["src_bytes"])
    dst_bytes = int(data["dst_bytes"])

    features = np.array([[duration, src_bytes, dst_bytes]])

    prediction = model.predict(features)[0]

    print("Prediction:", prediction)

    return jsonify({
        "prediction": str(prediction)
    })

if __name__ == "__main__":
    app.run(debug=True)