from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.ingestion import run_bronze_pipeline
from src.transformation import run_silver_pipeline
from src.features import run_gold_pipeline
from src.load_to_db import run_loader_pipeline

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

    run_silver_task = PythonOperator(
        task_id="run_silver_pipeline",
        python_callable=run_silver_pipeline,
    )

    run_gold_task = PythonOperator(
        task_id="run_gold_pipeline",
        python_callable=run_gold_pipeline,
    )

    load_to_db_task = PythonOperator(
        task_id="load_to_db",
        python_callable=run_loader_pipeline,
    )

    run_bronze_task >> run_silver_task >> run_gold_task >> load_to_db_task