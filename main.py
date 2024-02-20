from calcoloTDEE import calculate_tdee

height = float(input("Inserisci l'altezza in cm: "))
weight = float(input("Inserisci il peso in kg: "))
age = int(input("Inserisci l'età: "))
gender = input("Inserisci il genere (M o F): ")
activity_level = input("Inserisci il livello di attività (sedentary, lightly_active, moderately_active, hard_worker): ")

tdee = calculate_tdee(height, weight, age, gender, activity_level)

print(f"Il tuo TDEE è: {tdee} kcal")