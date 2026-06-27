import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Visualização de Elenco - Copa do Mundo",
    page_icon="⚽",
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

st.markdown('<div class="main-title">⚽ Seleção Brasileira - Copa do Mundo</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Artilharia do Elenco</div>', unsafe_allow_html=True)

df = pd.read_csv("dados/jogadores_brasil_convocados_copa_2026.csv")

df['data_nascimento'] = pd.to_datetime(df['data_nascimento'])
df['idade'] = df['data_nascimento'].apply(lambda x: (pd.Timestamp.now() - x).days // 365)

df_gols = df.sort_values(by='gols', ascending=True)

fig_gols = px.bar(
    df_gols,
    x='gols',
    y='nome',
    orientation='h',
    title='Quantidade de Gols por Atleta',
    labels={'gols': 'Gols Marcados', 'nome': 'Jogador'},
    color='gols',
    color_continuous_scale=['#ffdf00', '#009c3b']
)

fig_gols.update_layout(
    title_x=0.5,
    xaxis_title="Gols",
    yaxis_title="Jogador",
    height=700, 
    coloraxis_showscale=False 
)

st.plotly_chart(fig_gols, use_container_width=True)

st.markdown("---")

st.subheader("📋 Lista de Jogadores")

colunas_tabela = [
    'numero', 'nome', 'posicao', 'idade', 'jogos', 'gols', 'clube',
    'cartoes_amarelos_copa', 'cartoes_vermelhos_copa', 'wikipedia_jogador', 'wikipedia_clube'
]

st.dataframe(
    df[colunas_tabela],
    use_container_width=True,
    hide_index=True
)

