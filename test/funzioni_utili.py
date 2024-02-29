import cv2
import pymongo
from pyzbar import pyzbar
from openai import OpenAI

def spesana_ia(prompt):
    client = pymongo.MongoClient("mongodb+srv://projectwork:daita12@cluster0.hqm86xs.mongodb.net/")
    db = client["SpeSana"]
    chat = db["Chat.Ia"]
    risultato = list(chat.find())
    key = risultato[0]["key"]

    if key is None:
        raise ValueError("L'API Key di OpenAI non è stata configurata correttamente.")
    client = OpenAI(api_key=key)

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return str(chat_completion.choices[0].message.content)


def calculate_tdee(height, weight, age, gender, activity_level, goal):
    activity_factors = {
        "Sedentario": 1.2,
        "Leggermente attivo": 1.375,
        "Moderatamente attivo": 1.55,
        "Molto Attivo": 1.725
    }

    goal_factors = {
        "Dimagrire": 0.8,  # Sottrai il 20%
        "Mantenersi in forma": 1.0,  # Nessuna variazione
        "Aumentare la massa muscolare": 1.15  # Aggiungi il 15%
    }

    if gender == "M":
        bmr = 66.5 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
    else:
        bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)

    tdee_base = round(bmr * activity_factors.get(activity_level))
    tdee = round(tdee_base * goal_factors[goal])
    return tdee


def correct_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def codice_img(file):
    img = cv2.imread(file)
    barcodes = pyzbar.decode(img)
    for barcode in barcodes:
        barcode_info = barcode.data.decode('utf-8')
        if barcode_info.isdigit():
            return barcode_info

    return None

