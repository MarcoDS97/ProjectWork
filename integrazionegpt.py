import os
from openai import OpenAI
key = "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"
client = OpenAI(api_key=key)
prompt = """
Ciao, ho bisogno di un nutrizionista. Il mio obiettivo è dimagrire
mi dici un vantaggio e uno svantaggi nel comprare gli fagioli Borlotti?
"""
chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)


print(chat_completion)
print(str(chat_completion.choices[0].message.content))

