import os

from openai import OpenAI
key = ""
client = OpenAI()
prompt = "In base a la informazioni sul prodotto, il nome: nutella, indicami 1 ricetta di pasto che potrei fare se i miei obiettivi sono: diversiones, cucina in familia"
chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)


print(chat_completion)

