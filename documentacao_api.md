# Guia e Documentação da API-Sports - Copa do Mundo

Esta documentação serve como referência para entender os endpoints disponíveis na **API-Sports (API-Football)** e como consumi-los utilizando Python para extrair informações focadas **exclusivamente na Seleção Brasileira** (`team=6`).

---

## 🔑 Configuração Base

Para qualquer requisição à API-Sports, você precisa enviar a sua chave de autenticação nos cabeçalhos (headers) da requisição.

* **Base URL**: `https://v3.football.api-sports.io`
* **Header de Autenticação**: `x-apisports-key: SUA_CHAVE_API`
* **ID da Copa do Mundo (World Cup)**: `league=1`
* **ID da Seleção Brasileira**: `team=6`

---

## 📋 Endpoints Principais (Filtro para o Brasil)

### 1. Elenco de Jogadores da Seleção (`/players`)
Retorna a lista completa de atletas convocados para a Copa, com idade, peso, altura, foto e estatísticas detalhadas.
* **Endpoint**: `/players`
* **Parâmetros**: `team=6` (Brasil) e `season=2026` (ou a temporada desejada).
* **Exemplo de URL**: `GET https://v3.football.api-sports.io/players?team=6&season=2026`

### 2. Jogos e Calendário do Brasil (`/fixtures`)
Retorna as partidas agendadas, resultados, placares e status dos jogos (data, hora, estádio).
* **Endpoint**: `/fixtures`
* **Parâmetros**: `league=1` (Copa), `season=2026` e `team=6` (filtra apenas os jogos do Brasil).
* **Exemplo de URL**: `GET https://v3.football.api-sports.io/fixtures?league=1&season=2026&team=6`

### 3. Informações da Seleção e Estádio (`/teams`)
Retorna os dados cadastrais do time (código FIFA, fundação, logo) e o estádio principal associado.
* **Endpoint**: `/teams`
* **Parâmetros**: `id=6` (Brasil)
* **Exemplo de URL**: `GET https://v3.football.api-sports.io/teams?id=6`

### 4. Técnico da Seleção (`/coachs`)
Retorna a ficha técnica do treinador atual da equipe, idade, histórico de carreira e nacionalidade.
* **Endpoint**: `/coachs`
* **Parâmetros**: `team=6` (Brasil)
* **Exemplo de URL**: `GET https://v3.football.api-sports.io/coachs?team=6`

### 5. Classificação da Copa (`/standings`)
Exibe a tabela dos 12 grupos do torneio. Útil para verificar em qual grupo o Brasil está e sua posição em tempo real.
* **Endpoint**: `/standings`
* **Parâmetros**: `league=1` e `season=2026`
* **Exemplo de URL**: `GET https://v3.football.api-sports.io/standings?league=1&season=2026`

---

## 🐍 Exemplos Práticos de Implementação em Python

Abaixo estão os scripts para você rodar diretamente usando a biblioteca `requests`.

### Exemplo 1: Baixar os Jogos do Brasil na Copa do Mundo
Este script faz uma chamada direta para coletar todas as partidas da Seleção Brasileira na Copa de 2026.

```python
import requests

API_KEY = "chave"
BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}

# Parâmetros: Copa do Mundo (league=1), Ano 2026 e Time Brasil (team=6)
params = {
    "league": 1,
    "season": 2026,
    "team": 6
}

response = requests.get(f"{BASE_URL}/fixtures", headers=headers, params=params)

if response.status_code == 200:
    dados = response.json()
    partidas = dados.get("response", [])
    print(f"Total de jogos encontrados: {len(partidas)}")
    for p in partidas:
        confronto = f"{p['teams']['home']['name']} vs {p['teams']['away']['name']}"
        data_jogo = p['fixture']['date']
        status = p['fixture']['status']['long']
        print(f"Jogo: {confronto} | Data: {data_jogo} | Status: {status}")
else:
    print(f"Erro na requisição: {response.status_code}")
```

### Exemplo 2: Baixar Estatísticas dos Jogadores do Brasil
Este script baixa os jogadores da seleção brasileira e as estatísticas gerais deles.

```python
import requests

API_KEY = "chave"
BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "team": 6,
    "season": 2026
}

response = requests.get(f"{BASE_URL}/players", headers=headers, params=params)

if response.status_code == 200:
    dados = response.json()
    jogadores = dados.get("response", [])
    for j in jogadores:
        nome = j['player']['name']
        idade = j['player']['age']
        posicao = j['statistics'][0]['games']['position']
        print(f"Nome: {nome} | Idade: {idade} | Posição: {posicao}")
else:
    print(f"Erro na requisição: {response.status_code}")
```
