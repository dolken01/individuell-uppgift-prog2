from flask import Flask, render_template, request
import json


app = Flask(__name__)

@app.route("/") #Skapar route /
def index():
    return render_template("main.html")

@app.route("/priser")#Skapar route /priser
def prices():
    return "Sida som ska visa priser"