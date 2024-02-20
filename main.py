from calcoloTDEE import calculate_tdee

height = float(input("Inserisci l'altezza in cm: "))
weight = float(input("Inserisci il peso in kg: "))
age = int(input("Inserisci l'età: "))
gender = input("Inserisci il genere (M o F): ")
activity_level = input("Inserisci il livello di attività (sedentario, leggermente_attivo, moderatamente_attivo, molto_attivo): ")
goal = input("Inserisci l'obiettivo (dimagrire, mantenersi_in_forma, aumentare_massa_muscolare): ")

tdee = calculate_tdee(height, weight, age, gender, activity_level, goal)

print(f"Il tuo TDEE è: {tdee} kcal")