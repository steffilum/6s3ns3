from flask import Flask, jsonify, request
from Components.package_imports import *
from Components.benchmark1_prediction import benchmark1_prediction
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/mean_model_prediction', methods = ["POST", "GET"])
def mean_model_prediction():
    data = request.get_json(silent = True)
    selected_month = data["month"]
    selected_year = data["year"]
    selected_date = datetime.strptime(f"{selected_year}-{selected_month}-01", format = "%Y-%b-%d").strftime("%Y-%m-%d")
    pass
    # output = benchmark1_prediction(selected_date)
    # output = output.to_json()
    # return app.response_class(response = output, status = 200, mimetype= "application/json")

@app.route('/arft04_model_prediction', methods = ["POST", "GET"])
def arft04_model_prediction():
    data = request.get_json(silent = True)
    selected_month = data["month"]
    selected_year = data["year"]
    selected_date = datetime.strptime(f"{selected_year}-{selected_month}-01", format = "%Y-%b-%d").strftime("%Y-%m-%d")
    pass
    # output = arft04_model_prediction(selected_date)
    # output = output.to_json()
    # return app.response_class(response = output, status = 200, mimetype = "application/json")

@app.route('/midas_model_prediction', methods = ["POST", "GET"])
def midas_model_prediction():
    data = request.get_json(silent = True)
    selected_month = data["month"]
    selected_year = data["year"]
    selected_date = datetime.strptime(f"{selected_year}-{selected_month}-01", format = "%Y-%b-%d").strftime("%Y-%m-%d")
    pass
    # output = midas_model_prediction(selected_date)
    # output = output.to_json()
    # return app.response_class(response = output, status = 200, mimetype = "application/json")

@app.route('/bridge_model_prediction', methods = ["POST", "GET"])
def bridge_model_prediction():
    data = request.get_json(silent = True)
    selected_month = data["month"]
    selected_year = data["year"]
    selected_date = datetime.strptime(f"{selected_year}-{selected_month}-01", format = "%Y-%b-%d").strftime("%Y-%m-%d")
    pass
    # output = bridge_model_prediction(selected_date)
    # output = output.to_json()
    # return app.response_class(response = output, status = 200, mimetype = "application/json")

@app.route('/rf_model_prediction', methods = ["POST", "GET"])
def rf_model_prediction():
    data = request.get_json(silent = True)
    selected_month = data["month"]
    selected_year = data["year"]
    selected_date = datetime.strptime(f"{selected_year}-{selected_month}-01", format = "%Y-%b-%d").strftime("%Y-%m-%d")
    pass
    # output = rf_model_prediction(selected_date)
    # output = output.to_json()
    # return app.response_class(response = output, status = 200, mimetype = "application/json")

if __name__ == "__main__":
    app.run(debug = True)