# Copilot / AI Agent Instructions for ScalableETL

This repository provisions an AKS-based Airflow deployment and provides a small CSV-driven ETL DAG for scalability experiments. Keep guidance short, actionable and specific to files and workflows found here.

- **Big picture**: Terraform (root `terraform/`) provisions Azure resources (resource group, storage account, AKS). Kubernetes manifests for Airflow resources (StorageClass, PVC, HPA, DAGs) live in `terraform/` as YAML. The ETL DAG is `terraform/etl_pipeline.py` and reads `terraform/sales.csv` from the DAGs data path.

- **Key files**:
  - `terraform/main.tf` — Azure infra (AKS, storage, Event Grid stub).
  - `terraform/values.yaml` — Helm/values-like settings for Airflow workers and Postgres image.
  - `terraform/azurefile-sc.yaml` — StorageClass used by PVC.
  - `terraform/airflow-pvc.yaml` — PVC name `airflow-dags-pvc`; mounts DAGs/data into Airflow pods.
  - `terraform/airflow-hpa.yaml` — HPA targeting `StatefulSet` named `airflow-worker` (min 1 / max 5, CPU utilization target 20%).
  - `terraform/etl_pipeline.py` — Airflow DAG `etl_pipeline_csv` (manual trigger).

- **What an agent should assume**:
  - The DAG expects data at `/opt/airflow/dags/data/` inside Airflow pods (the DAG reads/writes CSVs using absolute paths).
  - The project uses Azure Files for shared DAG storage (StorageClass `azurefile`) and a PVC named `airflow-dags-pvc`.
  - Terraform may include protections (e.g., `prevent_destroy` on storage account) — avoid destructive changes.

- **Common developer workflows & commands** (run from repo root or `terraform/`):
  - Provision infra: run `terraform init` then `terraform apply` in `terraform/`.
  - Inspect pods: `kubectl get pods -n airflow`.
  - Forward Airflow web UI: `kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow`.
  - Trigger DAG from scheduler pod: `kubectl exec -n airflow <scheduler-pod> -- airflow dags trigger etl_pipeline_csv`.
  - Tail logs: `kubectl logs -n airflow <pod-name> -c <container>`.

- **Integration points & patterns**:
  - Event Grid integration exists as a commented block in `main.tf` that would webhook into an Airflow REST endpoint; if enabling, ensure Airflow API auth/URL matches expectations.
  - Postgres is used as Airflow metadata DB (image configured in `terraform/values.yaml`).
  - Autoscaling is applied at the worker StatefulSet level; HPA uses CPU utilization (20%) — tests may require lowering/raising this for experiments.

- **Project-specific conventions**:
  - DAGs and test data are packaged under `terraform/` so the IaC folder doubles as the deployment bundle for Airflow in this repo.
  - ETL tasks use simple PythonOperators with XComs referencing task ids: e.g., `ti.xcom_pull(task_ids='extract_task')`.
  - Hard-coded absolute file paths are used inside the DAG (`/opt/airflow/dags/data/`) — update PVC/mounts rather than DAG paths where possible.

- **What to avoid / watch for**:
  - Do not change the storage account `prevent_destroy` without confirmation — it is intentional for data safety.
  - The HPA targets a StatefulSet named `airflow-worker`; if resources/replica types change, update the HPA manifest accordingly.
  - Values in `values.yaml` (worker CPU/memory) directly impact autoscaling behaviour in experiments.

- **HPA troubleshooting & requirements**:
  - HPA using resource metrics requires two things: a working `metrics-server` and a CPU `requests` value on every container in the target pods. If any container lacks `requests.cpu`, the HPA will report `cpu: <unknown>/...` and cannot compute utilization.
  - Quick checks (run from your workstation):
    - `kubectl get deployment metrics-server -n kube-system`
    - `kubectl top pods -n airflow`
    - `kubectl describe hpa airflow-worker-hpa -n airflow`
    - `kubectl get pod <pod-name> -n airflow -o jsonpath='{.spec.containers[*].resources}'`
  - Quick fixes:
    - Add CPU requests to any container missing them. In this repo we added `workers.logGroomer.resources` to `terraform/values.yaml` so Helm/Terraform-deployed charts set requests for the `worker-log-groomer` sidecar.
    - Immediate, live patch (no redeploy) example:
      - `kubectl patch statefulset airflow-worker -n airflow --type='json' -p '[{"op":"add","path":"/spec/template/spec/containers/1/resources","value":{"requests":{"cpu":"50m","memory":"128Mi"},"limits":{"cpu":"200m","memory":"256Mi"}}}]'`
  - After changes, verify metrics and HPA status:
    - `kubectl top pods -n airflow`
    - `kubectl get hpa -n airflow -w`
  - Notes: prefer changing `terraform/values.yaml` (or Helm values) so the fix persists across redeploys. See `terraform/values.yaml` for the `workers` block.

- **If you need to modify or add a DAG**:
  - Add the DAG file to `terraform/` and test locally inside a container that mirrors Airflow mounts, or push it to the PVC-backed DAGs directory on the cluster.
  - Ensure the DAG's file paths match `/opt/airflow/dags/data/` (or update PVC mounts), and keep `schedule=None` for manual experiments unless scheduling is intended.

Keep changes minimal and document any infra changes in `terraform/` and README.md. If any behavior or config is unclear, ask for the runtime environment details (AKS version, Helm chart used, and how Airflow images are built/pulled).

---
Please review this brief guide and tell me which sections need more detail or examples. I'll iterate quickly.
