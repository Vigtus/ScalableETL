from airflow import DAG
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os
import tempfile

STORAGE_ACCOUNT = os.environ["AZURE_STORAGE_ACCOUNT"]
STORAGE_KEY = os.environ["AZURE_STORAGE_KEY"]

INPUT_CONTAINER = "input"
OUTPUT_CONTAINER = "output"
INPUT_BLOB = "sales.csv"
OUTPUT_BLOB = "sales_processed.csv"


def extract_transform_load():
    hook = WasbHook(
        wasb_conn_id=None,
        login=STORAGE_ACCOUNT,
        password=STORAGE_KEY
    )

    with tempfile.TemporaryDirectory() as tmp:
        input_path = f"{tmp}/input.csv"
        output_path = f"{tmp}/output.csv"

        # --- EXTRACT ---
        hook.get_file(
            file_path=input_path,
            container_name=INPUT_CONTAINER,
            blob_name=INPUT_BLOB
        )

        # --- TRANSFORM ---
        df = pd.read_csv(input_path)
        df["total_price"] = df["price"] * df["quantity"]
        df.to_csv(output_path, index=False)

        # --- LOAD ---
        hook.load_file(
            file_path=output_path,
            container_name=OUTPUT_CONTAINER,
            blob_name=OUTPUT_BLOB,
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
        python_callable=extract_transform_load,
    )
