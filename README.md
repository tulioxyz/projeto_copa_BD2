# Projeto Copa BD2 - Solução Analítica para a Seleção Brasileira

## 📋 Contexto do Projeto

Você foi contratado(a) como Analista de Dados da Seleção Brasileira e integra a equipe responsável por apoiar o processo de preparação para a Copa do Mundo. 

A comissão técnica deseja utilizar dados para tomar decisões mais estratégicas relacionadas à convocação, análise de desempenho, preparação física, estudo de adversários e acompanhamento da evolução do time ao longo da competição.

Seu desafio será projetar e implementar uma solução analítica completa, desde a coleta e integração dos dados até a construção de um dashboard interativo.

---

## 🛠️ Fontes de Dados Utilizadas

Para atender aos requisitos mínimos de fontes de dados, o projeto consome:
1. **GitHub Squads JSON**: Arquivo JSON com informações completas e tratadas da Seleção Brasileira da Copa de 2026.
2. **API Externa (API-Sports)**: Configuração estruturada para consumo de dados de desempenho da copa de 2022.

---

## 🚀 Como Executar o Projeto (Passo a Passo)

Siga os passos abaixo para configurar o ambiente virtual, instalar as bibliotecas necessárias e rodar a aplicação:

### Passo 1: Ativar o Ambiente Virtual (venv)
Caso já tenha a pasta `.venv` criada no projeto, ative o ambiente virtual executando o comando correspondente:

**No Linux/macOS:**
```bash
source .venv/bin/activate
```

**No Windows:**
```bash
.venv\Scripts\activate
```



### Passo 2: Instalar as Bibliotecas Necessárias
Com o ambiente virtual ativado, instale as dependências (Pandas, Streamlit, Requests, Plotly) listadas no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Passo 3: Executar a Coleta e Atualização de Dados
Para buscar os dados brutos e gerar o CSV tratado de convocados, execute o script de extração:
```bash
python extrair.py
```

### Passo 4: Inicializar o Dashboard do Streamlit
Para visualizar o dashboard interativo no seu navegador:
```bash
streamlit run app.py
```

---

## 📁 Estrutura de Arquivos

* `dados/` - Pasta contendo o CSV com o elenco estruturado da Seleção Brasileira.
* `app.py` - Script do dashboard do Streamlit contendo os KPIs, gráficos em Plotly e tabelas.
* `extrair.py` - Script para baixar o JSON bruto da internet e gerar o arquivo CSV de dados consolidados.
* `requirements.txt` - Lista de dependências de bibliotecas Python.