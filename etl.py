import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px

# conectar ao banco

conn = sqlite3.connect(r'')
df = pd.read_sql('SELECT * FROM precos', conn)

# tratando os dados

df['timestamp'] = pd.to_datetime(df['timestamp'])
df['data'] = df['timestamp'].dt.date

# streamlit 

st.set_page_config(page_title='Painel Cripto', layout='wide')
st.title('📊 Painel de Monitoramento - Criptomoedas')

datas = df['data'].unique()
data_selecionada = st.selectbox('Selecione a data:', sorted(datas, reverse=True))
df_filtrado = df[df['data'] == data_selecionada]

st.subheader('Resumo por moeda')

moedas = df_filtrado['moeda'].unique()
colunas = st.columns(len(moedas))

for i, moeda in enumerate(moedas):
    valor = df_filtrado[df_filtrado['moeda'] == moeda]['preco_usd'].mean()
    variacao = df_filtrado[df_filtrado['moeda'] == moeda]['variacao_24h'].mean()
    colunas[i].metric(label=moeda.capitalize(), value=f"R$ {valor:,.2f}", delta=f"{variacao:.2f}%")

moeda_grafico = st.selectbox('Selecione a moeda para visualizar o gráfico:', sorted(df['moeda'].unique()))
df_moeda = df[df['moeda'] == moeda_grafico]

fig = px.line(df_moeda, x='timestamp', y='preco_usd', title=f'Preço da {moeda_grafico.upper()} ao longo do tempo', labels={
    'timestamp': 'Data',
    'preco_usd': 'Preço (USD)'
})

st.plotly_chart(fig, use_container_width=True)






