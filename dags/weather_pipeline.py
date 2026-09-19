from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.ingestion import run_bronze_pipeline

with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2024, 6, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    run_bronze_task = PythonOperator(
        task_id="run_bronze_pipeline",
        python_callable=run_bronze_pipeline,
    )