from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import time
import os

def transform(task_id):
    duration = int(os.getenv("TRANSFORM_DURATION", 60))
    print(f"Transform {task_id} started")
    time.sleep(duration)
    print(f"Transform {task_id} finished")

with DAG(
    dag_id="etl_scaling_test",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=10,
    concurrency=20,
    tags=["scaling", "keda", "test"],
) as dag:

    transforms = []

    for i in range(20):
        t = PythonOperator(
            task_id=f"transform_{i}",
            python_callable=transform,
            op_args=[i],
        )
        transforms.append(t)
