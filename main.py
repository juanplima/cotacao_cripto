import os
from airflow import DAG 
from airflow.operators.python import PythonOperator
from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook
from datetime import datetime, timedelta 
import sqlite3
import requests
from pathlib import Path  

def send_slack_notification(message):
    slack_hook = SlackWebhookHook(
        slack_webhook_conn_id='slack_conn'
    )
    slack_hook.send(text=message, username='airflow-bot')

def inserir_dados():
    # conexão com o banco de dados
    base_dir = Path(__file__).resolve().parent
    db_path = base_dir / 'prices.db'
    print("Caminho absoluto:", os.path.abspath(db_path))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

# fazendo a requisição da api

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",  
        "vs_currencies": "usd",     
        "include_24hr_change": "true"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # criando a tabela 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS precos (
        timestamp TEXT,
        moeda TEXT,
        preco_usd REAL,
        variacao_24h REAL
    )
    ''')

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # inserindo os dados

    for moeda, info in data.items():
            preco = info.get('usd')
            variacao = info.get('usd_24h_change')
            cursor.execute('''
                INSERT INTO precos (timestamp, moeda, preco_usd, variacao_24h)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, moeda, preco, variacao))

    conn.commit()
    conn.close()
    print(f"[{timestamp}] Dados inseridos com sucesso em: {db_path}")
    
    msg = f"✅ Dados de criptomoedas inseridos com sucesso!\n⏰ {timestamp}\n"

    for moeda, info in data.items():
        preco = info.get('usd')
        variacao = info.get('usd_24h_change')
        msg += f"💰 *{moeda.title()}*: ${preco:.2f} (24h: {variacao:.2f}%)\n"

    send_slack_notification(msg)

# chamando o airflow 
with DAG(
    "inserir_dados_tabela",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args={
        'owner': 'airflow',
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    }
) as dag:

    atualizar_task = PythonOperator(
        task_id="inserir_dados_tabela",
        python_callable=inserir_dados,
    )

atualizar_task

