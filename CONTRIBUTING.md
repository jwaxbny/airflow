# CONTRIBUTING

## Overview

How to contribute to this project.

## How to run

```sh
# Start docker-compose
airflow > sh ./start.sh

# Stop docker-compose
airflow > sh ./stop.sh

# Restart docker-compose (if you change airflow.cfg)
airflow > sh ./restart.sh
```

## How to test DAG

```sh
# docker ps -> get scheduler containers ID

airflow> docker exec -it 07f64f532b63 /bin/bash
# airflow@07f64f532b63:/opt/airflow$

airflow@07f64f532b63:/opt/airflow$ > airflow tasks test sample_srh_flow_v_1_0_0 print_date 2022-01-01

```
