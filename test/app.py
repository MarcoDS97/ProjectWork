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
    a = list(
        prodotti.find({"nutriscore_grade": "a", "unique_scans_n": {"$gte": 100}}).sort("nutriscore_score").limit(10))
    b = list(prodotti.find(
        {"nutriscore_grade": "b", "nutriscore_score": {"$gte": 0, "$lte": 2}, "unique_scans_n": {"$gte": 100}}).sort(
        "nutriscore_score").limit(10))
    c = list(prodotti.find(
        {"nutriscore_grade": "c", "nutriscore_score": {"$gte": 3, "$lte": 10}, "unique_scans_n": {"$gte": 100}}).sort(
        "nutriscore_score").limit(10))
    d = list(prodotti.find(
        {"nutriscore_grade": "d", "nutriscore_score": {"$gte": 11, "$lte": 18}, "unique_scans_n": {"$gte": 100}}).sort(
        "nutriscore_score").limit(10))
    e = list(prodotti.find(
        {"nutriscore_grade": "e", "nutriscore_score": {"$gte": 19}, "unique_scans_n": {"$gte": 100}}).sort(
        "nutriscore_score").limit(10))
    nutriscore_home = [a, b, c, d, e]
    best = list(prodotti.find().sort("unique_scans_n", -1).limit(6))

    nome = ["Prodotti A Base Di Carne", "Bevande", "Latticini", "Snack Dolci"]
    categorie = [list(prodotti.find({"categories": n}).sort("unique_scans_n", -1).limit(10)) for n in nome]

    flagLog = False
    utente = []
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))

    if request.method == 'POST':
        dati_prompt = request.form.get('prompt')
        favorites = request.form.get('fav')
        search_hero = request.form.get('search_hero')
        search_modal = request.form.get('search_modal')

        if dati_prompt:
            dati_prompt = dati_prompt.split(", ")
            prodotto = list(prodotti.find({"code": dati_prompt[1]}))
            if dati_prompt[2] == "info":
                prompt = f"""
                Il mio obiettivo è {utente[0]["Goal"]} e il mio livello di attività è {utente[0]["activity_level"]}
                mi dici un vantaggio e uno svantaggio nel comprare questo prodotto: {prodotto[0]["product_name"]}?
                """
            else:
                prompt = f"""
                Il mio obiettivo è {utente[0]["Goal"]} e il mio livello di attività è {utente[0]["activity_level"]} 
                mi dici una ricetta corta per fare con {prodotto[0]["product_name"]}?
                """

            response = spesana_ia(prompt)
            return jsonify({'response': response})
        elif favorites:
            response = f"Ho aggiunto questo a i tuoi favoriti: {favorites}"
            return jsonify({'response': response})
        elif search_modal:
            return redirect(f"/search/{search_modal}")
        elif search_hero:
            return redirect(f"/search/{search_hero}")
        elif "code_hero" in request.files:
            codice = request.files['code_hero']
            if codice and codice != "":
                if correct_file(codice.filename):
                    filename = secure_filename(codice.filename)
                    codice.save(filename)
                    codice_barre = codice_img(codice.filename)
                    os.remove(codice.filename)
                    if codice_barre:
                        return redirect(f"/search/{codice_barre}")
                    else:
                        pass
        elif 'code_modal' in request.files:
            codice = request.files['code_modal']
            if codice and codice != "":
                if correct_file(codice.filename):
                    filename = secure_filename(codice.filename)
                    codice.save(filename)
                    print(codice_img(codice.filename))
                    os.remove(codice.filename)
    if utente:
        return render_template("home.html", lista_nutriscore=nutriscore_home, best=best, utente=utente[0],
                               flagLog=flagLog, categorie=categorie)
    else:
        return render_template("home.html", lista_nutriscore=nutriscore_home, best=best, flagLog=flagLog,
                               categorie=categorie)


@app.route("/search/<term>")
def search_term(term):
    flagLog = False
    utente = {}
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))
    if term.isdigit():
        products = list(prodotti.find({"code": term}).sort("unique_scans_n", -1))
    else:
        products = list(
            prodotti.find({"product_name": {"$regex": f".*{term}.*", "$options": "i"}}).sort("unique_scans_n", -1))
    page = int(request.args.get('page', 1))  # Ottiene il numero di pagina dalla query string, di default è 1
    per_page = 8  # Numero di elementi per pagina
    total_products = len(products)  # Numero totale di prodotti
    total_pages = (total_products + per_page - 1) // per_page
    offset = (page - 1) * per_page
    products = products[offset:offset + per_page]

    if utente:
        return render_template("search.html", prodotto=products, utente=utente[0], flagLog=flagLog, term=term,
                               current_page=page, total_pages=total_pages, max=max, min=min)
    else:
        return render_template("search.html", prodotto=products, flagLog=flagLog, current_page=page, term=term,
                               total_pages=total_pages, max=max, min=min)


@app.route("/product")
def product():
    flagLog = False
    utente = {}
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))
    prodotto = list(prodotti.find())
    page = int(request.args.get('page', 1))  # Ottiene il numero di pagina dalla query string, di default è 1
    per_page = 16  # Numero di elementi per pagina
    total_products = len(prodotto)  # Numero totale di prodotti
    total_pages = (total_products + per_page - 1) // per_page
    offset = (page - 1) * per_page
    products = prodotto[offset:offset + per_page]
    if utente:
        return render_template("products.html", prodotto=products, utente=utente[0], flagLog=flagLog, current_page=page,
                               total_pages=total_pages, max=max, min=min)
    else:
        return render_template("products.html", prodotto=products, flagLog=flagLog, current_page=page,
                               total_pages=total_pages, max=max, min=min)


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

    current_name = p[0].get("product_name", "")
    name = current_name.split()
    for n in name:
        related_products = list(prodotti.find({
                "code": {"$ne": codice},
                "product_name": {"$regex": f".*{n}.*", "$options": "i"}
            }).sort("unique_scans_n", -1).limit(3))
        if len(related_products) >= 1:
            break
    if request.method == 'POST':
        if prompt_ricetta:
            response = f"Ho ricevuto dati per fare il prompt: {prompt_ricetta}"
            return jsonify({'response': response})
        elif prompt_info:
            response = f"Ho ricevuto dati per fare il prompt: {prompt_info}"
            return jsonify({'response': response})
        # return jsonify({'response': (prompt_ricetta, prompt_info)})
    if utente:
        return render_template("product-detail.html", prodotto=p[0], utente=utente[0], flagLog=flagLog, len=len, related_products=related_products)
    else:
        return render_template("product-detail.html", prodotto=p[0], flagLog=flagLog, len=len, related_products=related_products)


@app.route("/login", methods=["POST", "GET"])
def login():
    signup_success = request.args.get("signup_success")
    verifica = True
    flagLog = False
    utente = []
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))

    if request.method == "POST":
        email = request.form.get("email_login")
        login_user = list(users.find({"Email": email}))
        if login_user:
            password_login = bytes(request.form.get("password_login"), 'utf-8')
            password_db = login_user[0]['Password']
            if bcrypt.checkpw(password=password_login, hashed_password=password_db):
                session['name'] = email
                return redirect("/")
            else:
                verifica = False

    if utente:
        return render_template("login.html", utente=utente[0], flagLog=flagLog, signup_success=signup_success,
                               verifica=verifica)
    else:
        return render_template("login.html", flagLog=flagLog, signup_success=signup_success, verifica=verifica)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    verifica = True
    flagLog = False
    utente = {}
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))

    if request.method == "POST":
        email = request.form.get('email_signup')

        if len(list(users.find({'Email': email}))) == 0:
            nome = request.form.get('nome_signup')
            cognome = request.form.get('cognome_signup')
            sesso = request.form.get('genere_signup')
            eta = request.form.get('eta_signup')
            altezza = request.form.get('altezza_signup')
            peso = request.form.get('peso_signup')
            obiettivo = request.form.get('obiettivo_signup')
            livello_attivita = request.form.get('livello_attivita_signup')
            categorie = [request.form.get(f'categoria{i}') for i in range(8) if
                         request.form.get(f'categoria{i}') is not None]

            password_coperta = bcrypt.hashpw(request.form.get('password_signup').encode('utf-8'), bcrypt.gensalt())

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
                'TDEE': tdee,
                'products_favorites': [],
                'recipes': []
            }
            )
            return redirect(url_for('login', signup_success=True))
        elif len(list(users.find({'Email': email}))) > 0:
            verifica = False
            # response = "Email già esistente"
            # return jsonify({'response': response})
    if utente:
        return render_template("signup.html", utente=utente[0], flagLog=flagLog, verifica=verifica)
    else:
        return render_template("signup.html", flagLog=flagLog, verifica=verifica)


@app.route("/profilo", methods=["POST", "GET"])
def profilo():
    flagLog = False
    utente = {}
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))

    cambio_password = None
    cambio_dati = None
    if request.method == "POST":

        password_old = request.form.get('password_old')
        password_new = request.form.get('password_new')

        email = request.form.get('email_profilo')
        nome = request.form.get('nome_profilo')
        cognome = request.form.get('cognome_profilo')
        sesso = request.form.get('genere_profilo')
        eta = request.form.get('eta_profilo')
        altezza = request.form.get('altezza_profilo')
        peso = request.form.get('peso_profilo')
        obiettivo = request.form.get('obiettivo_profilo')
        livello_attivita = request.form.get('livello_profilo')
        categorie = [request.form.get(f'categoria{i}_profilo') for i in range(8) if
                     request.form.get(f'categoria{i}_profilo') is not None]

        filtro = {"_id": utente[0]["_id"]}

        if password_old and password_new:
            password_verifica = bytes(password_old, 'utf-8')
            password_db = utente[0]['Password']
            print("ciao")
            if bcrypt.checkpw(password=password_verifica, hashed_password=password_db):
                password_new = bcrypt.hashpw(password_new.encode('utf-8'), bcrypt.gensalt())
                aggiornamento = {"$set": {'Password': password_new}}
                users.update_one(filtro, aggiornamento)
                cambio_password = True
                print(True)
            else:
                cambio_password = False
                print(False)
        else:
            new_data = {"Name": nome,
                        "Surname": cognome,
                        "Email": email,
                        "Gender": sesso,
                        "Age": eta,
                        "Height": altezza,
                        "Weight": peso,
                        "Favorites": categorie,
                        "Goal": obiettivo,
                        "activity_level": livello_attivita,
                        "TDEE": calculate_tdee(altezza, peso, eta, sesso, livello_attivita, obiettivo)}

            if new_data["Email"] != utente[0]["Email"]:
                if len(list(users.find({'Email': email}))) > 0:
                    cambio_dati = False
                else:
                    for key in new_data.keys():
                        if utente[0][key] != new_data[key]:
                            aggiornamento = {"$set": {key: new_data[key]}}
                            users.update_one(filtro, aggiornamento)
                    session["name"] = email
                    cambio_dati = True
            else:
                for key in new_data.keys():
                    if utente[0][key] != new_data[key]:
                        aggiornamento = {"$set": {key: new_data[key]}}
                        users.update_one(filtro, aggiornamento)
                session["name"] = email
                cambio_dati = True


    categorie = ["Cereali e patate", "Legumi", "Formaggi", "Prodotti A Base Di Carne",
                 "Cibi A Base Di Frutta E Verdura", "Latticini", "Biscotti", "Cibi E Bevande A Base Vegetale"]

    if utente:
        return render_template("profilo.html", utente=utente[0], flagLog=flagLog, categorie=categorie, cambio_password=cambio_password, cambio_dati=cambio_dati)
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


@app.route("/nutriscore")
def nutriscore():
    flagLog = False
    utente = {}
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))

    if utente:
        return render_template("nutriscore.html", utente=utente[0], flagLog=flagLog)
    else:
        return render_template("nutriscore.html", flagLog=flagLog)


if __name__ == '__main__':
    app.run(debug=True)
