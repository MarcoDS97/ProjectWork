import base64
import bcrypt

encoded_string = 'JDJiJDEyJDMvbXZQbEp2TER6Q3lYSFptbzFRV2VCcS5RY0lvLm53THRNOWNHOEtNSkdHbUE3OHE4YTFX'
decoded_bytes = base64.b64decode(encoded_string)
decoded_string = decoded_bytes.decode('utf-8')  # Decodifica i byte in una stringa UTF-8

# Hash della password memorizzato nel database
stored_hash = decoded_string.encode('utf-8')

# Password fornita dall'utente (da verificare)
user_password = 'benny998'

# Confronto tra la password fornita dall'utente e l'hash memorizzato
if bcrypt.checkpw(user_password.encode('utf-8'), stored_hash):
    print("Password corretta!")
else:
    print("Password incorretta.")