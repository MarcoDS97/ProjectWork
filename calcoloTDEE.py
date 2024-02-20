from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def calculate_tdee(height, weight, age, gender, activity_level, goal):

    activity_factors = {
        "sedentario": 1.2,
        "leggermente_attivo": 1.375,
        "moderatamente_attivo": 1.55,
        "molto_attivo": 1.725
    }

    goal_factors = {
        "dimagrire": 0.8,  # Sottrai il 20%
        "mantenersi_in_forma": 1.0,  # Nessuna variazione
        "aumentare_massa_muscolare": 1.15  # Aggiungi il 15%
    }

    if gender == "M":
        bmr = 66.5 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
    else:
        bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)

    tdee_base = round(bmr * activity_factors.get(activity_level))
    tdee = round(tdee_base * goal_factors[goal])
    return tdee

# Route per la pagina di registrazione
@app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    if request.method == 'POST':

        height = float(request.form['height'])
        weight = float(request.form['weight'])
        age = int(request.form['age'])
        gender = request.form['gender']
        activity_level = request.form['activity_level']
        goal = request.form['goal']
        tdee = calculate_tdee(height, weight, age, gender, activity_level, goal)

        # Aggiungere il TDEE al profilo dell'utente (questo è un esempio, devi implementare la tua logica di storage)
        # profile = get_user_profile()  # Funzione ipotetica per ottenere il profilo dell'utente
        # profile['tdee'] = tdee
        # save_user_profile(profile)  # Funzione ipotetica per salvare il profilo dell'utente

        return redirect(url_for('dashboard'))  # Reindirizza l'utente alla dashboard dopo la registrazione

    return render_template('registrazione.html')  # La pagina di registrazione con il modulo

if __name__ == '__main__':
    app.run(debug=True)
