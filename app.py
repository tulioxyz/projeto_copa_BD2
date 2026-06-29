import os
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Visualização de Elenco - Seleção Brasileira",
    layout="wide"
)

st.markdown("""
    <style>
        .stApp {
            background-color: #0f0f0f;
            color: #ffffff;
        }

        [data-testid="stSidebar"] {
            background-color: #141416 !important;
            border-right: 1px solid rgba(0, 156, 59, 0.15);
        }

        div[data-baseweb="select"] {
            background-color: #0f0f0f !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #0f0f0f !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
        }
        span[data-baseweb="tag"] {
            background-color: #009c3b !important;
            color: #ffffff !important;
        }

        h1 {
            color: #009c3b;
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -1px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        h2, h3, h4 {
            color: #ffffff;
        }

        .kpi-box {
            background: linear-gradient(135deg, #1a1a1a, #252525);
            border: 1px solid #009c3b;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }

        .kpi-number {
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffdf00;
        }

        .kpi-label {
            font-size: 0.9rem;
            color: #a0c0a0;
            margin-top: 4px;
        }

        [data-testid="column"] {
            display: flex !important;
            flex-direction: column !important;
        }
        [data-testid="column"] > div[data-testid="stVerticalBlock"] {
            display: flex !important;
            flex-direction: column !important;
            flex-grow: 1 !important;
            height: 100% !important;
        }
        [data-testid="column"] > div[data-testid="stVerticalBlock"] > div.element-container {
            display: flex !important;
            flex-direction: column !important;
            flex-grow: 1 !important;
            height: 100% !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #141416 !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px !important;
            padding: 20px !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5) !important;
            margin-bottom: 20px !important;
            display: flex !important;
            flex-direction: column !important;
            flex-grow: 1 !important;
            height: 100% !important;
            overflow: hidden !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            border: none !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {
            display: flex !important;
            flex-direction: column !important;
            flex-grow: 1 !important;
            height: 100% !important;
        }

        .stPlotlyChart {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin-bottom: 0 !important;
            overflow: hidden !important;
            flex-grow: 1 !important;
        }
        .stPlotlyChart > div {
            overflow: hidden !important;
        }

        .stDataFrame {
            background-color: #141416 !important;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 10px;
        }

        hr {
            border-color: #009c3b;
            opacity: 0.3;
        }
    </style>
""", unsafe_allow_html=True)


# carregamento dos dados
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

# filtros interativos
st.sidebar.markdown("## Filtros")
st.sidebar.markdown("Use os filtros abaixo para explorar o elenco:")

posicoes_disponiveis = sorted(df["posicao"].unique())
posicoes_escolhidas = st.sidebar.multiselect(
    "Posição",
    options=posicoes_disponiveis,
    default=posicoes_disponiveis
)

idade_min = int(df["idade"].min())
idade_max = int(df["idade"].max())
intervalo_idade = st.sidebar.slider(
    "Intervalo de Idade",
    min_value=idade_min,
    max_value=idade_max,
    value=(idade_min, idade_max)
)

clubes_disponiveis = sorted(df["clube"].unique())
clubes_escolhidos = st.sidebar.multiselect(
    "Clube",
    options=clubes_disponiveis,
    default=clubes_disponiveis
)

df_filtrado = df[
    (df["posicao"].isin(posicoes_escolhidas)) &
    (df["idade"] >= intervalo_idade[0]) &
    (df["idade"] <= intervalo_idade[1]) &
    (df["clube"].isin(clubes_escolhidos))
]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**{len(df_filtrado)} jogadores** encontrados com os filtros aplicados.")

# dashboard
st.markdown("<h1 style='text-align: center;'>Seleção Brasileira - Copa do Mundo</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #b3b3b3; font-weight: bold;'>Análise estatística e de desempenho do elenco convocado</p>", unsafe_allow_html=True)
st.markdown("---")

# KPIS
st.markdown("### Indicadores Gerais do Elenco")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-number">{len(df_filtrado)}</div>
            <div class="kpi-label">Jogadores Selecionados</div>
        </div>
    """, unsafe_allow_html=True)

media_idade = df_filtrado["idade"].mean() if not df_filtrado.empty else 0
with col2:
    st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-number">{media_idade:.1f}</div>
            <div class="kpi-label">Idade Média</div>
        </div>
    """, unsafe_allow_html=True)

total_jogos = df_filtrado["jogos"].sum() if not df_filtrado.empty else 0
with col3:
    st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-number">{total_jogos:,}</div>
            <div class="kpi-label">Total de Jogos</div>
        </div>
    """, unsafe_allow_html=True)

total_gols = df_filtrado["gols"].sum() if not df_filtrado.empty else 0
with col4:
    st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-number">{total_gols:,}</div>
            <div class="kpi-label">Total de Gols</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# api
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
def get_all_players_wc2022(api_key):
    if not api_key:
        return []
    all_players = []
    for page in [1, 2, 3]:
        res_json = fetch_team_players(api_key, 2022, page)
        if res_json:
            all_players.extend(res_json.get("response", []))
    return all_players

def get_top10_detailed_stats(top10_names):
    api_key = os.getenv("API_KEY")
    if not api_key and "API_KEY" in st.secrets:
        api_key = st.secrets["API_KEY"]
        
    all_players = get_all_players_wc2022(api_key)
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
    api_key = os.getenv("API_KEY")
    if not api_key and "API_KEY" in st.secrets:
        api_key = st.secrets["API_KEY"]
        
    all_players = get_all_players_wc2022(api_key)
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


# graficos
if df_filtrado.empty:
    st.warning("Nenhum jogador encontrado com os filtros selecionados.")
else:
    col_graf1, col_graf2 = st.columns(2)

    # Top 10 Maiores Goleadores
    with col_graf1:
        with st.container(border=True):
            st.markdown("#### Top 10 Maiores Goleadores")
            top10 = df_filtrado.sort_values(by="gols", ascending=False).head(10)
            
            fig_top10 = px.bar(
                top10,
                x="gols",
                y="nome",
                orientation="h",
                text="gols",
                color="gols",
                labels={"nome": "Jogador", "gols": "Gols"},
                color_continuous_scale=['#009c3b', '#ffdf00']
            )
            fig_top10.update_layout(
                yaxis=dict(categoryorder="total ascending"),
                xaxis=dict(showgrid=True, gridcolor='rgba(128, 128, 128, 0.2)', griddash='dash', range=[0, 80]),
                coloraxis_showscale=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#ffffff",
                height=450,
                margin=dict(l=130, r=20, t=25, b=25)
            )
            st.plotly_chart(fig_top10, use_container_width=True)

    # Quantidade de Jogadores por Posição
    with col_graf2:
        with st.container(border=True):
            st.markdown("#### Quantidade de Jogadores por Posição")
            grafico_posicao = df_filtrado["posicao"].value_counts().reset_index()
            grafico_posicao.columns = ["Posição", "Quantidade"]
            
            fig_posicao = px.bar(
                grafico_posicao,
                x="Posição",
                y="Quantidade",
                text="Quantidade",
                color="Posição",
                color_discrete_sequence=['#009c3b', '#ffdf00', '#002776', '#a5a5a5']
            )
            fig_posicao.update_layout(
                yaxis_title="Quantidade de Jogadores",
                showlegend=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#ffffff",
                height=450,
                margin=dict(l=40, r=20, t=25, b=25)
            )
            st.plotly_chart(fig_posicao, use_container_width=True)

    st.markdown("---")
    col_graf3, col_graf4 = st.columns(2)

    # Desempenho Detalhado do Top 5 Goleadores Na Última Copa do Mundo (2022)
    with col_graf3:
        with st.container(border=True):
            st.markdown("#### Desempenho Detalhado do Top 5 Goleadores na Copa 2022")
            top5_names_list = top10["nome"].head(5).tolist()
            df_detalhado = get_top10_detailed_stats(top5_names_list)
            
            if not df_detalhado.empty:
                metricas_disponiveis = df_detalhado["Métrica"].unique().tolist()
                metricas_selecionadas = st.multiselect(
                    "Filtrar métricas:",
                    options=metricas_disponiveis,
                    default=metricas_disponiveis,
                    key="multiselect_metricas"
                )
                
                df_filtrado_detalhado = df_detalhado[df_detalhado["Métrica"].isin(metricas_selecionadas)].copy()
                df_filtrado_detalhado["Texto"] = df_filtrado_detalhado["Quantidade"].astype(str)
                
                fig_detalhado = px.bar(
                    df_filtrado_detalhado,
                    x="Jogador",
                    y="Quantidade",
                    color="Métrica",
                    barmode="group",
                    text="Texto",
                    labels={"Quantidade": "Quantidade", "Jogador": "Jogador", "Métrica": "Métrica"},
                    color_discrete_sequence=['#009c3b', '#ffdf00', '#002776', '#a5a5a5', '#90caf9', '#ff9800']
                )
                fig_detalhado.update_traces(
                    textposition="outside",
                    textangle=0
                )
                fig_detalhado.update_layout(
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.35,
                        xanchor="center",
                        x=0.5,
                        title=None
                    ),
                    xaxis=dict(tickangle=0, title=dict(text="Jogador", standoff=20)),
                    yaxis=dict(title=dict(text="Quantidade", standoff=20)),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#ffffff",
                    height=600,
                    margin=dict(l=70, r=20, t=25, b=100)
                )
                st.plotly_chart(fig_detalhado, use_container_width=True)
            else:
                st.info("Nenhuma métrica detalhada disponível na API para os jogadores selecionados.")

    # Avaliação de Desempenho (Notas) dos Convocados Atuais na Copa de 2022
    with col_graf4:
        with st.container(border=True):
            st.markdown("#### Avaliação de Desempenho (Notas) na Copa 2022")
            csv_names_list = df_filtrado["nome"].tolist()
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
                    range_x=[0, 8.2]
                )
                fig_notas.update_traces(
                    textposition="outside",
                    textangle=0
                )
                fig_notas.update_layout(
                    height=600,
                    coloraxis_showscale=False,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#ffffff",
                    margin=dict(l=150, r=20, t=25, b=65)
                )
                fig_notas.update_xaxes(
                    title=dict(text="Nota Média", standoff=15),
                    range=[0, 8.2],
                    autorange=False,
                    tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8],
                    showgrid=True,
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    griddash='dash'
                )
                fig_notas.update_yaxes(
                    title=dict(text="Jogador", standoff=15)
                )
                st.plotly_chart(fig_notas, use_container_width=True, theme=None)
                st.markdown("<div style='height: 85px;'></div>", unsafe_allow_html=True)
            else:
                st.info("Nenhuma nota disponível na API para os jogadores selecionados (não estiveram na Copa de 2022).")

st.markdown("---")
# Tabela: Informações Gerais do Elenco Atual
st.markdown("### Informações Gerais do Elenco")

df_tabela = df_filtrado[[
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

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#b3b3b3; font-size:0.8rem;'>"
    "Dashboard criado com Python + Streamlit + Plotly | "
    "Dados da Copa do Mundo de 2022 obtidos via API-Sports"
    "</p>",
    unsafe_allow_html=True
)
