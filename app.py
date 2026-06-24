from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from urllib.parse import quote_plus
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("model.pkl")

# MongoDB Atlas
username = "CloudShieldAI"
password = quote_plus("cloudshield1234")
MONGO_URI = "mongodb+srv://CloudShieldAI:Cloud1234@cluster0.knbcq78.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)
try:
    client.admin.command('ping')
    print("MongoDB Connected Successfully")
except Exception as e:
    print("MongoDB Connection Failed:", e)


db = client["cloudshield"]
attack_logs = db["attack_logs"]


# ADD THIS HERE
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    duration = int(data["duration"])
    src_bytes = int(data["src_bytes"])
    dst_bytes = int(data["dst_bytes"])
    port = int(data["port"])

    if duration > 500:
        prediction = "dos"

    elif port in [21, 23, 4444]:
        prediction = "probe"

    elif src_bytes > 5000:
        prediction = "dos"

    else:
        prediction = "normal"

    return jsonify({
        "prediction": prediction
    })


@app.route("/save_log", methods=["POST"])
def save_log():

    data = request.json

    log_data = {
        "source_ip": data.get("source_ip"),
        "port": data.get("port"),
        "protocol": data.get("protocol"),
        "scenario": data.get("scenario"),
        "status": data.get("status"),
        "timestamp": datetime.now()
    }

    attack_logs.insert_one(log_data)

    return jsonify({
        "message": "Log saved successfully"
    })

@app.route("/testdb")
def testdb():

    attack_logs.insert_one({
        "test": "CloudShield connected",
        "time": datetime.now()
    })

    return "MongoDB working"


@app.route("/logs")
def logs():

    logs_data = list(
        attack_logs.find({}, {"_id": 0})
    )

    return jsonify(logs_data)


if __name__ == "__main__":
    app.run(debug=True)