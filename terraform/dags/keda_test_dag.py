from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import time

def heavy_task(i):
    print(f"Task {i} started")
    time.sleep(60)
    print(f"Task {i} finished")

with DAG(
    dag_id="keda_scaling_test",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    tasks = []
    for i in range(10):
        tasks.append(
            PythonOperator(
                task_id=f"task_{i}",
                python_callable=heavy_task,
                op_args=[i]
            )
        )
