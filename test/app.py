import json
import os
import bcrypt
import mysql.connector
import pymongo
from funzioni_utili import *
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_session import Session
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

client = pymongo.MongoClient("mongodb+srv://projectwork:daita12@cluster0.hqm86xs.mongodb.net/")
db = client["SpeSana"]
prodotti = db["Products"]
users = db["Users"]


@app.route("/", methods=["POST", "GET"])
def homepage():
    a = list(prodotti.find({"nutriscore_grade": "a", "unique_scans_n": {"$gte": 100}}).sort("nutriscore_score").limit(10))
    b = list(prodotti.find({"nutriscore_grade": "b", "nutriscore_score": {"$gte": 0, "$lte": 2 }, "unique_scans_n": {"$gte": 100}}).sort("nutriscore_score").limit(10))
    c = list(prodotti.find({"nutriscore_grade": "c", "nutriscore_score": {"$gte": 3, "$lte": 10}, "unique_scans_n": {"$gte": 100}}).sort("nutriscore_score").limit(10))
    d = list(prodotti.find({"nutriscore_grade": "d", "nutriscore_score": {"$gte": 11, "$lte": 18}, "unique_scans_n": {"$gte": 100}}).sort("nutriscore_score").limit(10))
    e = list(prodotti.find({"nutriscore_grade": "e", "nutriscore_score": {"$gte": 19}, "unique_scans_n": {"$gte": 100}}).sort("nutriscore_score").limit(10))
    nutriscore_home = [a, b, c, d, e]
    best = list(prodotti.find().sort("unique_scans_n", -1).limit(6))

    flagLog = False
    utente = {}
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))

    if request.method == 'POST':
        prompt = request.form.get('prompt')
        search_hero = request.form.get('search_hero')
        search_modal = request.form.get('search_modal')

        if prompt:
            response = f"Ho ricevuto dati per fare il prompt: {prompt}"
            return jsonify({'response': response})
        elif search_modal:
            print(search_modal)
        elif search_hero:
            print(search_hero)
        elif "code_hero" in request.files:
            codice = request.files['code_hero']
            if codice and codice != "":
                if correct_file(codice.filename):
                    filename = secure_filename(codice.filename)
                    codice.save(filename)
                    print(codice_img(codice.filename))
                    os.remove(codice.filename)

        elif 'code_modal' in request.files:
            codice = request.files['code_modal']
            if codice and codice != "":
                if correct_file(codice.filename):
                    filename = secure_filename(codice.filename)
                    codice.save(filename)
                    print(codice_img(codice.filename))
                    os.remove(codice.filename)
    if utente:
        return render_template("home.html", lista_nutriscore=nutriscore_home, best=best, utente=utente[0], flagLog=flagLog)
    else:
        return render_template("home.html", lista_nutriscore=nutriscore_home, best=best, flagLog=flagLog)


@app.route("/product/<codice>", methods=["POST", "GET"])
def product_codice(codice):
    p = list(prodotti.find({"code": codice}))
    prompt_ricetta = request.form.get('ricetta_p')
    prompt_info = request.form.get('info_p')

    flagLog = False
    utente = {}
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))

    if request.method == 'POST':
        if prompt_ricetta:
            response = f"Ho ricevuto dati per fare il prompt: {prompt_ricetta}"
            return jsonify({'response': response})
        elif prompt_info:
            response = f"Ho ricevuto dati per fare il prompt: {prompt_info}"
            return jsonify({'response': response})
        # return jsonify({'response': (prompt_ricetta, prompt_info)})

    if utente:
        return render_template("product-detail.html", prodotto=p[0], utente=utente[0], flagLog=flagLog)
    else:
        return render_template("product-detail.html", prodotto=p[0], flagLog=flagLog)


@app.route("/login", methods=["POST", "GET"])
def login():
    flagLog = False
    utente = {}
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))

    if request.method == "POST":
        email = request.form.get("email_login")
        password = bcrypt.hashpw(request.form.get("password_login").encode('utf-8'), bcrypt.gensalt())
        verifica = True
        if users.find({"Email": email}) and users.find({"Password": password}):
            session['name'] = email
            return redirect("/")
        else:
            verifica = False

    if utente:
        return render_template("login.html", utente=utente[0], flagLog=flagLog)
    else:
        return render_template("login.html", flagLog=flagLog)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    flagLog = False
    utente = {}
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))

    email = request.form.get('email_signup')
    if len(list(users.find({'Email': email}))) == 0:
        nome = request.form.get('nome_signup')
        cognome = request.form.get('cognome_signup')
        sesso = request.form.get('genere_signup')
        eta = int(request.form.get('eta_signup'))
        altezza = float(request.form.get('altezza_signup'))
        peso = float(request.form.get('peso_signup'))
        obiettivo = request.form.get('obiettivo_signup')
        livello_attivita = request.form.get('livello_attivita_signup')
        categorie = [request.form.get(f'categoria{i}') for i in range(8) if
                     request.form.get(f'categoria{i}') is not None]

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
            'Favorites': categorie,
            'Goal': obiettivo,
            'activity_level': livello_attivita,
            'TDEE': tdee
        }
        )
        return redirect('/')
    elif len(list(users.find({'Email': email}))) > 0:
        response = "Email già esistente"
        return jsonify({'response': response})
    if utente:
        return render_template("signup.html", utente=utente[0], flagLog=flagLog)
    else:
        return render_template("signup.html", flagLog=flagLog)


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
        nome = request.form.get('nome_signup')
        cognome = request.form.get('cognome_signup')
        sesso = request.form.get('genere_signup')
        eta = int(request.form.get('eta_signup'))
        altezza = float(request.form.get('altezza_signup'))
        peso = float(request.form.get('peso_signup'))
        obiettivo = request.form.get('obiettivo_signup')
        livello_attivita = request.form.get('livello_attivita_signup')
        categorie = [request.form.get(f'categoria{i}') for i in range(8) if request.form.get(f'categoria{i}') is not None]

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
            'Favorites': categorie,
            'Goal': obiettivo,
            'activity_level': livello_attivita,
            'TDEE': tdee
        }
        )
        return redirect('/')
    # elif len(list(users.find({'Email': email}))) > 0:
    #     response = "Email già esistente"
    #     return jsonify({'response': response})
    # return render_template('signupOld.html')

@app.route("/product")
def product():
    flagLog = False
    utente = {}
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))

    prodotto = list(prodotti.find({"brands": "Ferrero"}))
    if utente:
        return render_template("product.html", prodotto=prodotto, utente=utente[0], flagLog=flagLog)
    else:
        return render_template("product.html", prodotto=prodotto, flagLog=flagLog)

@app.route("/profilo")
def profilo():
    flagLog = False
    utente = {}
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))

    categorie = ["Cereali e patate", "Legumi", "Formaggi", "Prodotti A Base Di Carne", "Cibi A Base Di Frutta E Verdura", "Latticini", "Biscotti", "Cibi E Bevande A Base Vegetale"]
    if utente:
        return render_template("profilo.html", utente=utente[0], flagLog=flagLog, categorie=categorie)
    else:
        return render_template("profilo.html", flagLog=flagLog, categorie=categorie)

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
