from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os
from azure.storage.blob import BlobServiceClient
from io import StringIO


def extract_transform_load():
    print("ETL started")

    account = os.environ["AZURE_STORAGE_ACCOUNT"]
    key = os.environ["AZURE_STORAGE_KEY"]
    print("Azure credentials loaded")

    conn_str = (
        f"DefaultEndpointsProtocol=https;"
        f"AccountName={account};"
        f"AccountKey={key};"
        f"EndpointSuffix=core.windows.net"
    )

    blob_service = BlobServiceClient.from_connection_string(conn_str)
    print("Connected to Azure Blob Storage")

    input_container = "input"
    output_container = "output"
    input_blob = "sales.csv"
    output_blob = "sales_processed.csv"

    # --- DOWNLOAD ---
    blob_client = blob_service.get_blob_client(
        container=input_container,
        blob=input_blob
    )
    csv_data = blob_client.download_blob().readall().decode("utf-8")
    print("CSV downloaded from input blob")

    df = pd.read_csv(StringIO(csv_data))

    # --- TRANSFORM ---
    df["total"] = df["price"] * df["quantity"]
    print("Transformation finished")

        # 🔥 SYMULACJA CIĘŻKIEGO ZADANIA (KEDA MUSI TO ZOBACZYĆ)
    print("Simulating heavy processing (sleep 60s)")
    time.sleep(60)

    # --- UPLOAD ---
    out_csv = df.to_csv(index=False)

    out_blob_client = blob_service.get_blob_client(
        container=output_container,
        blob=output_blob
    )
    out_blob_client.upload_blob(out_csv, overwrite=True)
    print("CSV uploaded to output blob")

    print("ETL finished successfully")
    return True   


with DAG(
    dag_id="etl_blob_to_blob",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    task = PythonOperator(
        task_id="extract_transform_load",
        python_callable=extract_transform_load,
    )
