import json
import bcrypt
import mysql.connector
import pymongo
from funzioni_utili import *
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
client = pymongo.MongoClient("mongodb+srv://projectwork:daita12@cluster0.hqm86xs.mongodb.net/")
db = client["SpeSana"]
products = db["Products"]
users = db["Users"]


@app.route("/")
def homepage():
    a = list(products.find({"nutriscore_grade": "a"}).sort("nutriscore_score").limit(10))
    nutriscore_home = [a]
    best = list(products.find().sort("unique_scans_n", -1).limit(6))

    return render_template("home.html", lista_nutriscore=nutriscore_home, best=best)

@app.route("/product/<codice>")
def product_codice(codice):
    p = list(products.find({"code": codice}))

    return render_template("product-detail.html", prodotto=p[0])

@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    return render_template("signup.html")

@app.route("/gpt", methods=["POST", "GET"])
def gpt():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        print(prompt)
        response = "RISPOSTA"

        return jsonify({'response': response})
    return render_template('gpt-test.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email_signup')
    if len(list(users.find({'Email': email}))) == 0:
        # password = request.form.get('password_signup')
        nome = request.form.get('nome_signup')
        cognome = request.form.get('cognome_signup')
        sesso = request.form.get('genere_signup')
        eta = int(request.form.get('eta_signup'))
        altezza = float(request.form.get('altezza_signup'))
        peso = float(request.form.get('peso_signup'))
        obiettivo = request.form.get('obiettivo_signup')
        livello_attivita = request.form.get('livello_attivita_signup')

        password_scoperta = request.form.get('password_signup')
        password_coperta = bcrypt.hashpw(password_scoperta.encode('utf-8'), bcrypt.gensalt())

        tdee = calculate_tdee(altezza, peso, eta, sesso, livello_attivita, obiettivo)

        users.insert_one({
            'Email': email,
            'Password': password_coperta,
            'Name': nome,
            'Surname': cognome,
            'Gender': sesso,
            'Age': eta,
            'Height': altezza,
            'Weight': peso,
            'Favorites': [],
            'Goal': obiettivo,
            'Activity Level': livello_attivita,
            'TDEE': tdee
        }
        )
        return redirect('/')
    else:
        response = "Email già esistente"
        return jsonify({'response': response})
    return render_template('signupOld.html')


@app.route("/")
def index():
    # check if the users exist or not
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    return render_template('index.html')


@app.route("/product/old")
def product():
    prodotti = list(products.find({"brands": "Ferrero"}))

    return render_template("product.html", prodotti=prodotti)


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
