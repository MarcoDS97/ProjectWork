import cv2
from pyzbar import pyzbar


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
