from flask import Flask, render_template, request
import requests
import json
import pandas as pd
import ssl
from datetime import datetime, timedelta


app = Flask(__name__)

@app.route("/")
def index():
    """ The main page """
    return render_template("index.html") 

@app.route("/form")
def form():
    """ Create route /form """

    return render_template('form.html')

@app.route("/priser", methods=["GET", "POST"])
def api_el():
    """ Shows page with prices"""
    year = request.form.get("year")
    month = request.form.get("month")
    day = request.form.get("day")
    area = request.form.get("area")

    el_url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{area}.json"
    json_data = requests.get(el_url)
    data = json.loads(json_data.text)
    df = pd.DataFrame(data)
    df["time_start"] = pd.to_datetime(df["time_start"], errors="coerce")
    df["time_start"] = df["time_start"].dt.strftime("%H:%M")
    

    table_data = df.to_html(columns=["time_start", "SEK_per_kWh"], classes="table p-5", justify="left")
    return render_template("elpriser.html", price=table_data, year=year, month=month, day=day, area=area)