"""
### mydag_crawler_flow_v_1_0_0.py
Sample crawler Flow
"""
# [START import_module]
from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Utils
# from airflow.utils.helpers import cross_downstream
from airflow.utils.task_group import TaskGroup

# My Packages
from mypackage.mycommon.crawler_functions import _parse_files, _run_bash_parse_output

# [END import_module]


# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args={
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
# [END default_args]

# [START instantiate_dag]
with DAG(
    'mydag_crawler_flow_v_1_0_0',
    default_args=default_args,
    description='Sample crawler Flow DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 1, 1),
    catchup=False,
    tags=['mypackage'],
) as dag:
    # [END instantiate_dag]

    # [START DAG documentation]
    dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    # [END DAG documentation]

    # [START basic_task]
    # generate_version = PythonOperator(
    #     task_id='generate_version',
    #     python_callable=_generate_version
    # )


    get_version_task_cmd = """
    python3 -m mypackage.mycommon.modules.generate_version | tail -n 1
    """
    generate_version_task = PythonOperator(
        task_id="generate_version_task",
        provide_context=True,
        python_callable=_run_bash_parse_output,
        op_kwargs={'cmd': get_version_task_cmd}
    )

    get_file_list = BashOperator(
        task_id="get_file_list",
        bash_command='echo {"exit_code": 1, "version": 1640995200}'
    )
    # [END basic_task]

    # [START TASK documentation]
    generate_version_task.doc_md = dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)

    """
    )
    # [END TASK documentation]

    # [START jinja_template]
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
    {% endfor %}
    """
    )

    validate = BashOperator(
        task_id='validate',
        depends_on_past=False,
        bash_command=templated_command,
    )
    # [END jinja_template]

    # [START create x num of tasks]

    # for i in range(10):
    #     task_id = f'parse_files_{i}'
    #     parse_files = PythonOperator(
    #         task_id=task_id,
    #         op_args=[i],
    #         python_callable=_parse_files,
    #         dag=dag)
    #     generate_version >> parse_files >> validate

    # [END create x num of tasks]

    # [START create TaskGroup]

    with TaskGroup(group_id='parse_group') as parse_group:
        for i in range(1,11):
            task_id = f'parse_files_{i}'
            parse_files = PythonOperator(
                task_id=task_id,
                op_args=[i],
                python_callable=_parse_files,
                pool='parser_group_pool')

    # [END create TaskGroup]

    generate_version_task >> parse_group >> validate

if __name__ == "__main__":
	dag.cli()
# [END sample]