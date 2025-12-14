from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def extract():
    print("📥 Extracting data from source...")
    return "raw_data.csv"

def transform(**context):
    raw_file = context['ti'].xcom_pull(task_ids='extract_task')
    print(f"🔄 Transforming {raw_file}...")
    return "transformed_data.csv"

def load(**context):
    transformed_file = context['ti'].xcom_pull(task_ids='transform_task')
    print(f"📤 Loading {transformed_file} to destination...")

with DAG(
    'etl_pipeline',
    default_args={
        'owner': 'marta',
        'retries': 1,
        'retry_delay': timedelta(minutes=2),
    },
    description='Simple ETL example',
    schedule_interval=None,
    start_date=datetime(2025, 12, 1),
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load,
        provide_context=True
    )

    extract_task >> transform_task >> load_task
