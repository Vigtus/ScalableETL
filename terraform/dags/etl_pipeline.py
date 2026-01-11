from datetime import datetime, timedelta
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

def extract():
    df = pd.read_csv("/opt/airflow/dags/data/sales.csv")
    print(f"Extracted {len(df)} rows")
    df.to_csv("/opt/airflow/dags/data/raw_data.csv", index=False)
    return "/opt/airflow/dags/data/raw_data.csv"

def transform(**context):
    raw_file = context['ti'].xcom_pull(task_ids='extract_task')
    df = pd.read_csv(raw_file)
    result = df.groupby('category')['sales'].sum().reset_index()
    result.to_csv("/opt/airflow/dags/data/transformed.csv", index=False)
    print("Transformed data saved")
    return "/opt/airflow/dags/data/transformed.csv"

def load(**context):
    transformed_file = context['ti'].xcom_pull(task_ids='transform_task')
    df = pd.read_csv(transformed_file)
    print("Final data preview:")
    print(df.head())

with DAG(
    dag_id='etl_pipeline_csv',
    default_args={'owner': 'marta','retries': 1,'retry_delay': timedelta(minutes=2)},
    description='ETL pipeline for CSV test',
    schedule=None,
    start_date=datetime(2025, 12, 1),
    catchup=False,
) as dag:

    extract_task = PythonOperator(task_id='extract_task', python_callable=extract)
    transform_task = PythonOperator(task_id='transform_task', python_callable=transform)
    load_task = PythonOperator(task_id='load_task', python_callable=load)

    extract_task >> transform_task >> load_task
