import json
import os


with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

grupo_tecnico = data['config']

comments = data['comments']

ultima_interacao = comments[len(comments) - 1]

print(data['email_tech'])
print(data['sla_ticket'])
print(ultima_interacao['name_create'])
print(ultima_interacao['description'])
print(ultima_interacao['dt_cad'])