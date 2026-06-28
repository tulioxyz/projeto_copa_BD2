import os
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Visualização de Elenco - Copa do Mundo",
    layout="wide"
)

st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        color: #009c3b;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #002776;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Seleção Brasileira - Copa do Mundo</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Artilharia do Elenco Copa do Mundo 2026</div>', unsafe_allow_html=True)

# Carregar dados
df = pd.read_csv("dados/jogadores_brasil_convocados_copa_2026.csv")
df['data_nascimento'] = pd.to_datetime(df['data_nascimento'])
df['idade'] = df['data_nascimento'].apply(lambda x: (pd.Timestamp.now() - x).days // 365)

posicao_map = {
    "GK": "Goleiro",
    "DF": "Defensor",
    "MF": "Meio-campista",
    "FW": "Atacante"
}
df['posicao'] = df['posicao'].map(posicao_map).fillna(df['posicao'])

st.markdown("---")
# Gráfico: Top 10 Maiores Goleadores
st.markdown("<h3 style='text-align: center;'>Top 10 Maiores Goleadores</h3>", unsafe_allow_html=True)

top10 = df.sort_values(by="gols", ascending=False).head(10)

fig_top10 = px.bar(
    top10,
    x="gols",
    y="nome",
    orientation="h",
    text="gols",
    color="gols",
    labels={
        "nome": "Jogador",
        "gols": "Gols"
    }
)

fig_top10.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    xaxis=dict(showgrid=True),
    coloraxis_showscale=False
)

st.plotly_chart(fig_top10, use_container_width=True)

st.markdown("---")

# Gráfico: Quantidade de Jogadores por Posição
st.markdown("<h3 style='text-align: center;'>Quantidade de Jogadores por Posição</h3>", unsafe_allow_html=True)

grafico_posicao = df["posicao"].value_counts().reset_index()
grafico_posicao.columns = ["Posição", "Quantidade"]

fig_posicao = px.bar(
    grafico_posicao,
    x="Posição",
    y="Quantidade",
    text="Quantidade",
    color="Posição"
)

fig_posicao.update_layout(
    yaxis_title="Quantidade de Jogadores"
)

st.plotly_chart(fig_posicao, use_container_width=True)

st.markdown("---")
# Gráfico: Desempenho Detalhado do Top 5 Goleadores Na Última Copa do Mundo (2022)
st.markdown("<h3 style='text-align: center;'>Desempenho Detalhado do Top 5 Goleadores Na Última Copa do Mundo (2022)</h3>", unsafe_allow_html=True)

@st.cache_data(ttl=86400)
def fetch_team_players(api_key, season, page):
    import requests
    url = "https://v3.football.api-sports.io/players"
    headers = {"x-apisports-key": api_key}
    params = {"team": 6, "season": season, "page": page}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None

@st.cache_data(ttl=86400)
def get_all_players_wc2022():
    api_key = os.getenv("API_KEY")
    if not api_key:
        return []
    all_players = []
    for page in [1, 2, 3]:
        res_json = fetch_team_players(api_key, 2022, page)
        if res_json:
            all_players.extend(res_json.get("response", []))
    return all_players

def get_top10_detailed_stats(top10_names):
    all_players = get_all_players_wc2022()
    if not all_players:
        return pd.DataFrame()
        
    player_data = []
    
    for target_name in top10_names:
        totals = {
            "Partidas": 0,
            "Gols": 0,
            "Assistências": 0,
            "Chutes": 0,
            "Dribles": 0,
            "Passes": 0
        }
        found = False
        for p in all_players:
            p_name = p["player"]["name"] or ""
            p_first = p["player"].get("firstname") or ""
            p_last = p["player"].get("lastname") or ""
            full_name = f"{p_name} {p_first} {p_last}".lower()
            target_words = target_name.lower().split()
            if all(w in full_name for w in target_words):
                for stat in p["statistics"]:
                    if stat["team"]["id"] == 6 and stat["league"]["id"] == 1:
                        found = True
                        totals["Gols"] += stat["goals"].get("total") or 0
                        totals["Assistências"] += stat["goals"].get("assists") or 0
                        totals["Chutes"] += stat["shots"].get("total") or 0
                        totals["Dribles"] += stat["dribbles"].get("success") or 0
                        totals["Passes"] += stat["passes"].get("total") or 0
                        totals["Partidas"] += stat["games"].get("appearences") or 0
                        
        if found:
            for metric, val in totals.items():
                player_data.append({
                    "Jogador": target_name,
                    "Métrica": metric,
                    "Quantidade": val
                })
        else:
            for metric in totals.keys():
                player_data.append({
                    "Jogador": target_name,
                    "Métrica": metric,
                    "Quantidade": 0
                })
                
    return pd.DataFrame(player_data)

def get_players_ratings_wc2022(csv_names):
    all_players = get_all_players_wc2022()
    if not all_players:
        return pd.DataFrame()
        
    ratings_data = []
    
    for target_name in csv_names:
        found = False
        for p in all_players:
            p_name = p["player"]["name"] or ""
            p_first = p["player"].get("firstname") or ""
            p_last = p["player"].get("lastname") or ""
            full_name = f"{p_name} {p_first} {p_last}".lower()
            
            target_words = target_name.lower().split()
            if all(w in full_name for w in target_words):
                for stat in p["statistics"]:
                    if stat["team"]["id"] == 6 and stat["league"]["id"] == 1:
                        rating_str = stat["games"].get("rating")
                        apps = stat["games"].get("appearences") or 0
                        if apps > 0 and rating_str:
                            try:
                                rating_val = float(rating_str)
                                ratings_data.append({
                                    "Jogador": target_name,
                                    "Nota": round(rating_val, 2)
                                })
                                found = True
                                break
                            except ValueError:
                                pass
                if found:
                    break
                    
    df_ratings = pd.DataFrame(ratings_data)
    if not df_ratings.empty:
        df_ratings = df_ratings.sort_values(by="Nota", ascending=False)
    return df_ratings

top5_names_list = top10["nome"].head(5).tolist()

df_detalhado = get_top10_detailed_stats(top5_names_list)

if not df_detalhado.empty:
    metricas_disponiveis = df_detalhado["Métrica"].unique().tolist()
    metricas_selecionadas = st.multiselect(
        "Filtrar métricas:",
        options=metricas_disponiveis,
        default=metricas_disponiveis
    )
    
    df_filtrado = df_detalhado[df_detalhado["Métrica"].isin(metricas_selecionadas)].copy()
    df_filtrado["Texto"] = df_filtrado["Quantidade"].astype(str)
    
    fig_detalhado = px.bar(
        df_filtrado,
        x="Jogador",
        y="Quantidade",
        color="Métrica",
        barmode="group",
        text="Texto",
        labels={"Quantidade": "Quantidade na Copa 2022", "Jogador": "Jogador", "Métrica": "Métrica"},
        color_discrete_sequence=['#009c3b', '#ffdf00', '#002776', '#a5a5a5', '#90caf9', '#ff9800']
    )
    
    fig_detalhado.update_traces(
        textposition="outside",
        textangle=0
    )
    
    fig_detalhado.update_layout(
        xaxis_title="Jogador",
        yaxis_title="Quantidade",
        legend_title="Métrica",
        xaxis=dict(tickangle=0)
    )
    
    st.plotly_chart(fig_detalhado, use_container_width=True)

st.markdown("---")
# Gráfico: Avaliação de Desempenho (Notas) dos Convocados Atuais na Copa de 2022
st.markdown("<h3 style='text-align: center;'>Avaliação de Desempenho (Notas) dos Convocados na Copa de 2022</h3>", unsafe_allow_html=True)

csv_names_list = df["nome"].tolist()
df_notas = get_players_ratings_wc2022(csv_names_list)

if not df_notas.empty:
    df_notas = df_notas.sort_values(by="Nota", ascending=True)
    df_notas["Texto"] = df_notas["Nota"].astype(str)
    
    fig_notas = px.bar(
        df_notas,
        x="Nota",
        y="Jogador",
        orientation="h",
        text="Texto",
        color="Nota",
        color_continuous_scale=['#ffdf00', '#009c3b'],
        labels={"Nota": "Nota Média", "Jogador": "Jogador"},
        range_x=[0, 8]
    )
    
    fig_notas.update_traces(
        textposition="outside",
        textangle=0
    )
    
    fig_notas.update_layout(
        xaxis_title="Nota Média",
        yaxis_title="Jogador",
        height=600,
        coloraxis_showscale=False
    )
    
    fig_notas.update_xaxes(
        range=[0, 8],
        autorange=False,
        tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        showgrid=True,
        gridcolor='rgba(128, 128, 128, 0.2)',
        griddash='dash'
    )
    
    st.plotly_chart(fig_notas, use_container_width=True, theme=None)

st.markdown("---")
# Tabela: Informações Gerais do Elenco Atual
st.markdown("<h3 style='text-align: center;'>Informações Gerais do Elenco</h3>", unsafe_allow_html=True)

df_tabela = df[[
    'nome', 'numero', 'idade', 'clube', 'posicao', 
    'jogos', 'gols'
]].copy()

df_tabela = df_tabela.sort_values(by='nome', ascending=True)

df_tabela.columns = [
    'Nome', 'Número', 'Idade', 'Clube', 'Posição', 
    'Jogos na Seleção', 'Gols na Seleção'
]

st.dataframe(
    df_tabela,
    use_container_width=True,
    hide_index=True
)
