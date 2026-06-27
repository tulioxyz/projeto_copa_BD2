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

# Leitura direta do CSV
df = pd.read_csv("dados/jogadores_brasil_convocados_copa_2026.csv")

# Calcula a idade
df['dob'] = pd.to_datetime(df['dob'])
df['idade'] = df['dob'].apply(lambda x: (pd.Timestamp.now() - x).days // 365)

# Gráfico de barras horizontais bonito com todos os atletas ordenados por gols
df_gols = df.sort_values(by='goals', ascending=True)

fig_gols = px.bar(
    df_gols,
    x='goals',
    y='name',
    orientation='h',
    title='Quantidade de Gols por Atleta',
    labels={'goals': 'Gols Marcados', 'name': 'Jogador'},
    color='goals',
    color_continuous_scale=['#ffdf00', '#009c3b'] # Gradiente amarelo para verde
)

fig_gols.update_layout(
    title_x=0.5,
    xaxis_title="Gols",
    yaxis_title="Jogador",
    height=700, # Altura adequada para exibir todos os 26 jogadores claramente
    coloraxis_showscale=False # Esconde a barra de cores lateral para um visual mais limpo
)

st.plotly_chart(fig_gols, use_container_width=True)

st.markdown("---")

# Tabela direta
st.subheader("📋 Lista de Jogadores")
st.dataframe(df[['no', 'name', 'pos', 'idade', 'caps', 'goals', 'club']], use_container_width=True, hide_index=True)
