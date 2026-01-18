from airflow import DAG
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import io

def extract_transform_load():
    hook = WasbHook(wasb_conn_id="azure_blob_conn")

    # --- Extract ---
    csv_bytes = hook.read_file(
        container_name="input",
        blob_name="sales.csv"
    )

    df = pd.read_csv(io.BytesIO(csv_bytes))

    # --- Transform ---
    df["total"] = df["price"] * df["quantity"]

    # --- Load ---
    output_buffer = io.StringIO()
    df.to_csv(output_buffer, index=False)

    hook.load_string(
        data=output_buffer.getvalue(),
        container_name="output",
        blob_name="sales_processed.csv",
        overwrite=True
    )

with DAG(
    dag_id="etl_blob_to_blob",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "azure", "blob"],
) as dag:

    etl_task = PythonOperator(
        task_id="extract_transform_load",
        python_callable=extract_transform_load
    )
