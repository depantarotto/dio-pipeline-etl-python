import pandas as pd
import requests

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

# ------------ EXTRACT ----------------
df = pd.read_csv('SDW2023.csv')
user_ids = df['UserId'].tolist()
# print(user_ids)

users = []
for id in user_ids:
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    if response.status_code == 200:
        users.append(response.json())

# ---------- TRANSFORM ------------------

arquivo_do_excel = "Mensagem.xlsx"

arq_excel = pd.read_excel(arquivo_do_excel)

for idx, user in enumerate(users):
    serie_msg = arq_excel.loc[arq_excel["UserID"] == user["id"], "Mensagem"]
    msg_user = serie_msg.values[0]
    arq_excel.loc[arq_excel["UserID"] == user["id"], "Processado"] = "Sim"
    users[idx]['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": f'Olá {user["name"]}. {msg_user}'
    })

arq_excel.to_excel(arquivo_do_excel, index=False)

# ----------------- LOAD ------------------
for user in users:
    resposta = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    sucesso = "Sim" if resposta.status_code == 200 else "Não"
    print(f"Usuário {user['name']} foi atualizado? {sucesso}!")
