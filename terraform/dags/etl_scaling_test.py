from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import time
import os

# -------------------------
# TASK FUNCTIONS
# -------------------------

def extract():
    print("Extract step started")
    time.sleep(5)
    print("Extract step finished")

def transform():
    print("Transform step started - simulating heavy workload")

    # Symulacja długiego taska (blokuje workera)
    duration = int(os.getenv("TRANSFORM_DURATION", 60))
    time.sleep(duration)

    print("Transform step finished")

def load():
    print("Load step started")
    time.sleep(5)
    print("Load step finished")

# -------------------------
# DAG DEFINITION
# -------------------------

with DAG(
    dag_id="etl_scaling_test",
    start_date=datetime(2024, 1, 1),
    schedule=None,           # ręczne uruchamianie
    catchup=False,
    tags=["scaling", "keda", "test"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform,
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load,
    )

    extract_task >> transform_task >> load_task