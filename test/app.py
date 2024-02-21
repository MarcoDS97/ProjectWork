import json
import mysql.connector
import pymongo
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
client = pymongo.MongoClient("mongodb+srv://projectwork:daita12@cluster0.ajv3ccw.mongodb.net/")
db = client["SpeSana"]
products = db["Products"]
users = db["Users"]


# print(db)

@app.route("/")
def homepage():
    return render_template("provaCard2.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    return render_template("signup.html")


@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email_signup')
    password = request.form.get('password_signup')
    nome = request.form.get('nome_signup')
    cognome = request.form.get('cognome_signup')
    sesso = request.form.get('genere_signup')
    eta = request.form.get('eta_signup')
    altezza = request.form.get('altezza_signup')
    peso = request.form.get('peso_signup')
    obiettivo = request.form.get('peso_signup')
    livello_attivita = request.form.get('peso_signup')

    users.insert_one({
        'Email': email,
        'Password': password,
        'Name': nome,
        'Surname': cognome,
        'Gender': sesso,
        'Age': eta,
        'Height': altezza,
        'Weight': peso,
        'Favorites': [],
        'Goal': obiettivo,
        'Activity Level': livello_attivita,
    }
    )

    return 'Data inserted successfully!'


@app.route("/")
def index():
    # check if the users exist or not
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    return render_template('index.html')


@app.route("/product")
def product():
    prodotti = list(products.find({"brands": "Ferrero"}))

    return render_template("product.html", prodotti=prodotti)


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
