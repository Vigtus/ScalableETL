# ScalableETL

🧩 General Concept of the Project

The goal of this project is to design and test a scalable ETL (Extract – Transform – Load) architecture operating in a cloud environment.
The main focus is not on processing a specific type of data, but on engineering and evaluating the scalability, resilience, and performance of the entire data pipeline.

🎯 Project Objectives

The project demonstrates how modern cloud-native tools such as Docker, Kubernetes, Azure Data Factory, and Apache Airflow can work together to build a scalable and flexible ETL system.

🔍 Research and Testing Scope

The project focuses on analyzing and testing the following aspects of the ETL system:

Scalability – evaluating how the pipeline reacts to an increasing amount of input data (e.g., larger CSV files or more records).

Parallel Execution – assessing system behavior under concurrent ETL job execution.

Automatic Scaling (Auto-Scaling) – observing how Kubernetes (Horizontal Pod Autoscaler) dynamically increases the number of replicas under higher workload and how quickly it reacts to load changes.

Monitoring and Metrics – implementing an observability stack using Prometheus and Grafana to measure performance, CPU/RAM utilization, and processing time.

🧠 Key Goal

The project has a research-engineering character.
Its main outcomes include:

a practical demonstration of a scalable ETL process running in a containerized environment,

an analysis of how cluster configuration and parameters affect data processing efficiency,

documentation of results and recommendations for optimizing data pipelines in the cloud.
