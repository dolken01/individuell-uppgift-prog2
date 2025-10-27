from flask import Flask, render_template, request
import requests
import json
import pandas as pd
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

    try: # Fångar upp om användaren skriver fel format
        selected_date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
    except ValueError:
        return "Ogiltigt datumformat.", 400

    
    min_date = datetime(2022, 11, 1) # Sätter minsta datum man kan söka på
    max_date = datetime.now().date() + timedelta(days=1) # Sätter högsta datum man kan söka på

    if selected_date < min_date: # Felmedalande om användaren skriver för lågt datum
        return "För lågt datum. Du kan inte söka elpriser före 2022-11-01.", 400
    if selected_date.date() > max_date: # Felmedelande om användaren skriver datum för långt fram
        return "Du kan inte söka elpriser längre fram än imorgon.", 400


    el_url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{area}.json"
    json_data = requests.get(el_url) # Hämtar json
    data = json.loads(json_data.text) # laddar json
    df = pd.DataFrame(data)
    df["time_start"] = pd.to_datetime(df["time_start"], errors="coerce")
    df["time_start"] = df["time_start"].dt.strftime("%H:%M")
    

    table_data = df.to_html(columns=["time_start", "SEK_per_kWh"], classes="table p-5", justify="left")
    return render_template("elpriser.html", price=table_data, year=year, month=month, day=day, area=area)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error404.html")