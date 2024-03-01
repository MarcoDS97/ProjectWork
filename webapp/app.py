import os
import bcrypt
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


@app.route("/favorites", methods=["POST"])
def favorites():
    if session.get('name'):
        utente = list(users.find({'Email': session['name']}))
    if request.method == 'POST':
        data = request.json
        favorites = data["fav"]
        print(favorites)
        if favorites not in utente[0]['products_favorites']:
            users.update_one(
                {'Email': utente[0]['Email']},  # Filtra il documento in base all'ID
                {'$push': {'products_favorites': favorites}})
        else:
            users.update_one(
                {'Email': utente[0]['Email']},  # Filtra il documento in base all'ID
                {'$pull': {'products_favorites': favorites}})


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
    fail = False
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
                response = spesana_ia(prompt)
            else:
                prompt = f"""
                Il mio obiettivo è {utente[0]["Goal"]} e il mio livello di attività è {utente[0]["activity_level"]} 
                mi dici una ricetta corta da fare con {prodotto[0]["product_name"]}?
                """
                response = spesana_ia(prompt)
                users.update_one(
                    {'Email': utente[0]["Email"]},  # Filtra il documento in base all'ID
                    {'$push': {'recipes': [response, prodotto[0]["code"], prodotto[0]["product_name"]]}})

            return jsonify({'response': response})

        elif favorites:
            if favorites not in utente[0]['products_favorites']:
                users.update_one(
                    {'Email': utente[0]['Email']},  # Filtra il documento in base all'ID
                    {'$push': {'products_favorites': favorites}})
            else:
                users.update_one(
                    {'Email': utente[0]['Email']},  # Filtra il documento in base all'ID
                    {'$pull': {'products_favorites': favorites}})

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
                        fail = True

        elif 'code_modal' in request.files:
            codice = request.files['code_modal']
            if codice and codice != "":
                if correct_file(codice.filename):
                    filename = secure_filename(codice.filename)
                    codice.save(filename)
                    codice_barre = codice_img(codice.filename)
                    os.remove(codice.filename)
                    if codice_barre:
                        return redirect(f"/search/{codice_barre}")
                    else:
                        fail = True
    if utente:
        return render_template("home.html", lista_nutriscore=nutriscore_home, best=best, utente=utente[0],
                               flagLog=flagLog, categorie=categorie, fail=fail)
    else:
        return render_template("home.html", lista_nutriscore=nutriscore_home, best=best, flagLog=flagLog,
                               categorie=categorie, fail=fail)


@app.route("/search/<term>", methods=["POST", "GET"])
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
    sort_by = request.args.get('sortBy')
    if sort_by == 'no_popularity':
        products.sort(key=lambda x: x['unique_scans_n'])
    elif sort_by == 'a-z':
        products.sort(key=lambda x: x['product_name'])
    elif sort_by == 'nutriscore_up':
        products = [p for p in products if p['nutriscore_grade'] in ['a', 'b', 'c', 'd', 'e']]
        products.sort(key=lambda x: x['nutriscore_grade'])
    elif sort_by == 'nutriscore_down':
        products = [p for p in products if p['nutriscore_grade'] in ['a', 'b', 'c', 'd', 'e']]
        products.sort(key=lambda x: x['nutriscore_grade'], reverse=True)
    page = int(request.args.get('page', 1))  # Ottiene il numero di pagina dalla query string, di default è 1
    per_page = 16  # Numero di elementi per pagina
    total_products = len(products)  # Numero totale di prodotti
    total_pages = (total_products + per_page - 1) // per_page
    offset = (page - 1) * per_page
    products = products[offset:offset + per_page]

    fail = False
    if request.method == 'POST':
        search_modal = request.form.get('search_modal')
        dati_prompt = request.form.get('prompt')

        if search_modal:
            return redirect(f"/search/{search_modal}")

        elif 'code_modal' in request.files:
            codice = request.files['code_modal']
            if codice and codice != "":
                if correct_file(codice.filename):
                    filename = secure_filename(codice.filename)
                    codice.save(filename)
                    codice_barre = codice_img(codice.filename)
                    os.remove(codice.filename)
                    if codice_barre:
                        return redirect(f"/search/{codice_barre}")
                    else:
                        fail = True

        elif dati_prompt:
            dati_prompt = dati_prompt.split(", ")
            prodotto = list(prodotti.find({"code": dati_prompt[1]}))
            if dati_prompt[2] == "info":
                prompt = f"""
                        Il mio obiettivo è {utente[0]["Goal"]} e il mio livello di attività è {utente[0]["activity_level"]}
                        mi dici un vantaggio e uno svantaggio nel comprare questo prodotto: {prodotto[0]["product_name"]}?
                        """
                response = spesana_ia(prompt)
            else:
                prompt = f"""
                        Il mio obiettivo è {utente[0]["Goal"]} e il mio livello di attività è {utente[0]["activity_level"]} 
                        mi dici una ricetta corta da fare con {prodotto[0]["product_name"]}?
                        """
                response = spesana_ia(prompt)
                users.update_one(
                    {'Email': utente[0]["Email"]},  # Filtra il documento in base all'ID
                    {'$push': {'recipes': [response, prodotto[0]["code"], prodotto[0]["product_name"]]}})

            return jsonify({'response': response})

    if utente:
        return render_template("search.html", prodotto=products, utente=utente[0], flagLog=flagLog, term=term,
                               current_page=page, total_pages=total_pages, max=max, min=min, sortBy=sort_by, fail=fail)
    else:
        return render_template("search.html", prodotto=products, flagLog=flagLog, current_page=page, term=term,
                               total_pages=total_pages, max=max, min=min, sortBy=sort_by, fail=fail)


@app.route("/product", methods=["POST", "GET"])
def product():
    flagLog = False
    utente = {}
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))
    prodotto = list(prodotti.find())
    prodotto.sort(key=lambda x: x['unique_scans_n'], reverse=True)
    sort_by = request.args.get('sortBy')
    if sort_by == 'no_popularity':
        prodotto.sort(key=lambda x: x['unique_scans_n'])
    elif sort_by == 'a-z':
        prodotto.sort(key=lambda x: x['product_name'])
    elif sort_by == 'nutriscore_up':
        prodotto = [p for p in prodotto if p['nutriscore_grade'] in ['a', 'b', 'c', 'd', 'e']]
        prodotto.sort(key=lambda x: x['nutriscore_grade'])
    elif sort_by == 'nutriscore_down':
        prodotto = [p for p in prodotto if p['nutriscore_grade'] in ['a', 'b', 'c', 'd', 'e']]
        prodotto.sort(key=lambda x: x['nutriscore_grade'], reverse=True)
    page = int(request.args.get('page', 1))  # Ottiene il numero di pagina dalla query string, di default è 1
    per_page = 16  # Numero di elementi per pagina
    total_products = len(prodotto)  # Numero totale di prodotti
    total_pages = (total_products + per_page - 1) // per_page
    offset = (page - 1) * per_page
    products = prodotto[offset:offset + per_page]

    fail = False
    if request.method == 'POST':
        search_modal = request.form.get('search_modal')
        dati_prompt = request.form.get('prompt')

        if search_modal:
            return redirect(f"/search/{search_modal}")

        elif 'code_modal' in request.files:
            codice = request.files['code_modal']
            if codice and codice != "":
                if correct_file(codice.filename):
                    filename = secure_filename(codice.filename)
                    codice.save(filename)
                    codice_barre = codice_img(codice.filename)
                    os.remove(codice.filename)
                    if codice_barre:
                        return redirect(f"/search/{codice_barre}")
                    else:
                        fail = True

        elif dati_prompt:
            dati_prompt = dati_prompt.split(", ")
            prodotto = list(prodotti.find({"code": dati_prompt[1]}))
            if dati_prompt[2] == "info":
                prompt = f"""
                        Il mio obiettivo è {utente[0]["Goal"]} e il mio livello di attività è {utente[0]["activity_level"]}
                        mi dici un vantaggio e uno svantaggio nel comprare questo prodotto: {prodotto[0]["product_name"]}?
                        """
                response = spesana_ia(prompt)
            else:
                prompt = f"""
                        Il mio obiettivo è {utente[0]["Goal"]} e il mio livello di attività è {utente[0]["activity_level"]} 
                        mi dici una ricetta corta da fare con {prodotto[0]["product_name"]}?
                        """
                response = spesana_ia(prompt)
                users.update_one(
                    {'Email': utente[0]["Email"]},  # Filtra il documento in base all'ID
                    {'$push': {'recipes': [response, prodotto[0]["code"], prodotto[0]["product_name"]]}})

            return jsonify({'response': response})

    if utente:
        return render_template("products.html", prodotto=products, utente=utente[0], flagLog=flagLog, current_page=page,
                               total_pages=total_pages, max=max, min=min, sortBy=sort_by, fail=fail)
    else:
        return render_template("products.html", prodotto=products, flagLog=flagLog, current_page=page,
                               total_pages=total_pages, max=max, min=min, sortBy=sort_by, fail=fail)


@app.route("/product/<codice>", methods=["POST", "GET"])
def product_codice(codice):
    p = list(prodotti.find({"code": codice}))

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

    fail = False

    if request.method == 'POST':
        search_modal = request.form.get('search_modal')
        if search_modal:
            return redirect(f"/search/{search_modal}")

        elif 'code_modal' in request.files:
            codice = request.files['code_modal']
            if codice and codice != "":
                if correct_file(codice.filename):
                    filename = secure_filename(codice.filename)
                    codice.save(filename)
                    codice_barre = codice_img(codice.filename)
                    os.remove(codice.filename)
                    if codice_barre:
                        return redirect(f"/search/{codice_barre}")
                    else:
                        fail = True

    if utente:
        return render_template("product-detail.html", prodotto=p[0], utente=utente[0], flagLog=flagLog, len=len,
                               related_products=related_products, fail=fail)
    else:
        return render_template("product-detail.html", prodotto=p[0], flagLog=flagLog, len=len,
                               related_products=related_products, fail=fail)


@app.route("/login", methods=["POST", "GET"])
def login():
    signup_success = request.args.get("signup_success")
    verifica = True
    fail = False
    if session.get('name'):
        return redirect("/")

    if request.method == "POST":
        email = request.form.get("email_login")
        login_user = list(users.find({"Email": email}))
        search_modal = request.form.get('search_modal')

        if login_user:
            password_login = bytes(request.form.get("password_login"), 'utf-8')
            password_db = login_user[0]['Password']
            if bcrypt.checkpw(password=password_login, hashed_password=password_db):
                session['name'] = email
                return redirect("/")
            else:
                verifica = False

        elif search_modal:
            return redirect(f"/search/{search_modal}")

        elif 'code_modal' in request.files:
            codice = request.files['code_modal']
            if codice and codice != "":
                if correct_file(codice.filename):
                    filename = secure_filename(codice.filename)
                    codice.save(filename)
                    codice_barre = codice_img(codice.filename)
                    os.remove(codice.filename)
                    if codice_barre:
                        return redirect(f"/search/{codice_barre}")
                    else:
                        fail = True

    return render_template("login.html", signup_success=signup_success,
                           verifica=verifica, fail=fail)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    verifica = True
    fail = False
    if session.get('name'):
        return redirect("/")

    if request.method == "POST":
        email = request.form.get('email_signup')
        search_modal = request.form.get('search_modal')

        if email and len(list(users.find({'Email': email}))) == 0:
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

        elif search_modal:
            return redirect(f"/search/{search_modal}")

        elif 'code_modal' in request.files:
            codice = request.files['code_modal']
            if codice and codice != "":
                if correct_file(codice.filename):
                    filename = secure_filename(codice.filename)
                    codice.save(filename)
                    codice_barre = codice_img(codice.filename)
                    os.remove(codice.filename)
                    if codice_barre:
                        return redirect(f"/search/{codice_barre}")
                    else:
                        fail = True

    return render_template("signup.html", fail=fail, verifica=verifica)


@app.route("/profilo", methods=["POST", "GET"])
def profilo():
    if session.get('name'):
        flagLog = True
        preferiti = []
        utente = list(users.find({'Email': session['name']}))
        codici = utente[0]["products_favorites"]
        for codice in codici:
            prodotto = prodotti.find({"code": codice})
            nome = prodotto[0]["product_name"]
            preferiti.append([codice, nome])
        fail = False
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

            search_modal = request.form.get('search_modal')

            if password_old and password_new:
                password_verifica = bytes(password_old, 'utf-8')
                password_db = utente[0]['Password']

                if bcrypt.checkpw(password=password_verifica, hashed_password=password_db):
                    password_new = bcrypt.hashpw(password_new.encode('utf-8'), bcrypt.gensalt())
                    aggiornamento = {"$set": {'Password': password_new}}
                    users.update_one(filtro, aggiornamento)
                    cambio_password = True
                    print(True)
                    session["cambio_password"] = cambio_password
                    return redirect("/profilo")
                else:
                    cambio_password = False
                    print(False)
                    session["cambio_password"] = cambio_password
                    return redirect("/profilo")

            elif search_modal:
                return redirect(f"/search/{search_modal}")

            elif 'code_modal' in request.files:
                codice = request.files['code_modal']
                if codice and codice != "":
                    if correct_file(codice.filename):
                        filename = secure_filename(codice.filename)
                        codice.save(filename)
                        codice_barre = codice_img(codice.filename)
                        os.remove(codice.filename)
                        if codice_barre:
                            return redirect(f"/search/{codice_barre}")
                        else:
                            fail = True

            else:
                new_data = {"Name": nome,
                            "Surname": cognome,
                            "Email": email,
                            "Gender": sesso,
                            "Age": int(eta),
                            "Height": float(altezza),
                            "Weight": float(peso),
                            "Favorites": categorie,
                            "Goal": obiettivo,
                            "activity_level": livello_attivita,
                            "TDEE": calculate_tdee(float(altezza), float(peso), int(eta), sesso, livello_attivita,
                                                   obiettivo)}
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
            session["cambio_dati"] = cambio_dati
            return redirect('/profilo')

        categorie = ["Cereali e patate", "Legumi", "Formaggi", "Prodotti A Base Di Carne",
                     "Cibi A Base Di Frutta E Verdura", "Latticini", "Biscotti", "Cibi E Bevande A Base Vegetale"]
        cambio_dati = session.pop("cambio_dati", None)
        cambio_password = session.pop("cambio_password", None)
        return render_template("profilo.html", utente=utente[0], flagLog=flagLog, categorie=categorie,
                               cambio_password=cambio_password, cambio_dati=cambio_dati, len=len, preferiti=preferiti,
                               fail=fail)
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


@app.route("/profilo/ricette", methods=["POST", "GET"])
def profilo_ricette():
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))
        ricette = utente[0]["recipes"]
        fail = False

        if request.method == 'POST':
            search_modal = request.form.get('search_modal')
            if search_modal:
                return redirect(f"/search/{search_modal}")

            elif 'code_modal' in request.files:
                codice = request.files['code_modal']
                if codice and codice != "":
                    if correct_file(codice.filename):
                        filename = secure_filename(codice.filename)
                        codice.save(filename)
                        codice_barre = codice_img(codice.filename)
                        os.remove(codice.filename)
                        if codice_barre:
                            return redirect(f"/search/{codice_barre}")
                        else:
                            fail = True

        return render_template("ricette.html", utente=utente[0], flagLog=flagLog, ricette=ricette, len=len, fail=fail)
    else:
        return redirect("/login")


@app.route("/nutriscore", methods=["POST", "GET"])
def nutriscore():
    flagLog = False
    fail = False
    utente = {}
    if session.get('name'):
        flagLog = True
        utente = list(users.find({'Email': session['name']}))

    if request.method == 'POST':
        search_modal = request.form.get('search_modal')
        if search_modal:
            return redirect(f"/search/{search_modal}")

        elif 'code_modal' in request.files:
            codice = request.files['code_modal']
            if codice and codice != "":
                if correct_file(codice.filename):
                    filename = secure_filename(codice.filename)
                    codice.save(filename)
                    codice_barre = codice_img(codice.filename)
                    os.remove(codice.filename)
                    if codice_barre:
                        return redirect(f"/search/{codice_barre}")
                    else:
                        fail = True

    if utente:
        return render_template("nutriscore.html", utente=utente[0], flagLog=flagLog, fail=fail)
    else:
        return render_template("nutriscore.html", flagLog=flagLog, fail=fail)


if __name__ == '__main__':
    app.run(debug=True)

def runspesana():
    app.run()