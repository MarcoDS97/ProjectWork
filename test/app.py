import json
import mysql.connector
from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def homepage():

    return render_template("provaCard2.html")

@app.route("/action")
def action():

    return render_template("action.html")

if __name__ == '__main__':
    app.run(debug=True)