from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def calculate_tdee(height, weight, age, gender, activity_level):

    activity_factors = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "hard_worker": 1.725
    }

    if gender == "M":
        bmr = 66.5 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
    else:
        bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)

    tdee = round(bmr * activity_factors.get(activity_level), 2)
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

        tdee = calculate_tdee(height, weight, age, gender, activity_level)

        # Aggiungere il TDEE al profilo dell'utente (questo è un esempio, devi implementare la tua logica di storage)
        # profile = get_user_profile()  # Funzione ipotetica per ottenere il profilo dell'utente
        # profile['tdee'] = tdee
        # save_user_profile(profile)  # Funzione ipotetica per salvare il profilo dell'utente

        return redirect(url_for('dashboard'))  # Reindirizza l'utente alla dashboard dopo la registrazione

    return render_template('registrazione.html')  # La pagina di registrazione con il modulo

if __name__ == '__main__':
    app.run(debug=True)
