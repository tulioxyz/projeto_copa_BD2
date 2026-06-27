import os
import requests
import pandas as pd

# API-Sports
API_KEY = "3b317cf02218c6ab25fae3d8d61e2c17"
TEAM_ID = 6  
headers = {
    "x-apisports-key": API_KEY
}

os.makedirs('dados', exist_ok=True)

url = 'https://raw.githubusercontent.com/26worldcup/26worldcup.github.io/refs/heads/main/public/data/squads/BRA.json'

response = requests.get(url)
response.raise_for_status()
data = response.json()

df = pd.json_normalize(data['players'])

caminho_csv = os.path.join('dados', 'jogadores_brasil_convocados_copa_2026.csv')
df.to_csv(caminho_csv, index=False)
