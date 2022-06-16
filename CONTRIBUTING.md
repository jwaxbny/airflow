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

airflow@07f64f532b63:/opt/airflow$ > airflow tasks test mydag_crawler_flow_v_1_0_0 generate_version_task 2022-01-01

```

## How to package mypackage

1. install tools for packaging

```sh
(venv) airflow > pip install --upgrade pip setuptools wheel
```

2. Create setup.py file

3. Build the wheel (package)

```sh
(venv) airflow > python setup.py bdist_wheel
```


## How to debug mypackage

1. creat virtual environment

```sh
airflow > python3 -m venv ./venv
```

2. Debug python modules

```sh

airflow (venv)>  python3 -m debugpy --listen 5678 --wait-for-client -m dags.mypackage.mycommon.modules.generate_version

# vscode - Debug - Python Attach (See .vscode/launch.json)

```
