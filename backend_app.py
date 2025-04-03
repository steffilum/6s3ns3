from flask import Flask, jsonify, request
from Components.package_imports import *
from Components.benchmark1_prediction import benchmark1_prediction
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
import json

app = Flask(__name__)

@app.route('/mean_model_user_input', methods = ["POST", "GET"])
def mean_model_user_input():
    data = request.get_json(silent = True)
    selected_date = data["date"]
    output = benchmark1_prediction(selected_date)
    output = output.to_json()
    return app.response_class(response = output, status = 200, mimetype= "application/json")

if __name__ == "__main__":
    app.run(debug = True)