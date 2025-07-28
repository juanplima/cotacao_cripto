# 📈 Monitoramento de Criptomoedas com Python

Projeto pessoal para automatizar o monitoramento de criptomoedas (como Bitcoin e Ethereum), desde a coleta até visualização e notificação automatizada.

## 🔧 Tecnologias utilizadas

- 🐍 Python 3
- 🪙 API CoinGecko (para obter as cotações)
- 🛢️ SQLite + DBeaver (banco local)
- ⚙️ Apache Airflow (orquestração da DAG)
- 🔔 Slack (alertas automáticos com preços e variações)
- 📊 Streamlit (dashboard interativo)

## 🚀 Fluxo do Projeto

1. **etl.py** extrai as cotações da API da CoinGecko.
2. Os dados são armazenados no banco **prices.db** (SQLite).
3. O **main.py** define a DAG no Airflow, que roda automaticamente todos os dias.
4. Após a execução, um alerta formatado é enviado via Slack com as cotações.
5. O painel feito com **Streamlit** permite acompanhar o histórico de preços de forma visual e interativa.

## 📂 Estrutura do Projeto

