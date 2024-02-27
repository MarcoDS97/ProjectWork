from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://projectwork:SpeSana@cluster0.ajv3ccw.mongodb.net/'
mongo = PyMongo(app)

@app.route('/salva-dati', methods=['POST'])
def salva_dati():
    try:
        data = request.get_json()

        last_user = mongo.db.utenti.find_one(sort=[("user_id", -1)])
        last_user_id = last_user['user_id']

        new_user_id = last_user_id + 1


        email = data.get('email')
        nome = data.get('name')
        cognome = data.get('surname')
        username = data.get('username')
        password = data.get('password')
        eta = data.get('age')
        sesso = data.get('gender')
        altezza = data.get('height')
        peso = data.get('weight')
        livello_di_attivita_fisica = data.get('activity level')
        obiettivo = data.get('goal')

        mongo.db.utenti.insert_one({
            'user_id': new_user_id,
            'email': email,
            'name': nome,
            'surname': cognome,
            'username': username,
            'password': password,
            'age': eta,
            'gender': sesso,
            'height': altezza,
            'weight': peso,
            'activity level': livello_di_attivita_fisica,
            'goal': obiettivo
        })
        print({
            'UserID': new_user_id,
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
            'Activity Level': livello_di_attivita_fisica,
        })

        return jsonify({'message': 'Dati utente salvati con successo!'}), 201
    except Exception as e:
        print(e)
        return jsonify({'error': 'Errore nel salvataggio dei dati utente'}), 500


if __name__ == '__main__':
    app.run(debug=True)
