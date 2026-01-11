from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import time
import os

def heavy_task(task_id):
    duration = int(os.getenv("TRANSFORM_DURATION", 60))
    print(f"Task {task_id} started")
    time.sleep(duration)
    print(f"Task {task_id} finished")

with DAG(
    dag_id="etl_scaling_test",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=5,
    max_active_tasks=10,
    tags=["scaling", "keda", "test"],
) as dag:

    for i in range(10):
        PythonOperator(
            task_id=f"heavy_task_{i}",
            python_callable=heavy_task,
            op_args=[i],
        )
