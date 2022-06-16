#!/usr/bin/env python3

# DEBUG
# import debugpy
# debugpy.listen(("localhost", 5678))

# import std libs
import logging
import time
import json

# import airflow
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# import mypackage
import mypackage.mycommon.modules.generate_version as generate_version

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mypackage.mycommon.crawler_functions")

# [START python functions]

def _run_bash_parse_output(**kwargs):
    """
    calls BashOperator with kwards["cmd"]
    parses output, which should be json
    """
    result = 1
    try:
        cmd = kwargs["cmd"]
        bash_task = BashOperator(
            task_id = "run_bash_task",
            do_xcom_push = True,
            bash_command = cmd
        )
        output = bash_task.execute(context=kwargs)
        logger.debug(f'_run_bash_parse_output() type(output) = {type(output)}')
        logger.debug(f'_run_bash_parse_output() output = {output}')

        dict = json.loads(output)

        if "exit_code" in dict:
            result = dict["exit_code"]

        result = dict
    
    except ValueError as ve:
        logger.error(f'output is not json. result = 1', exc_info=ve)
        return result

    return result


# def _generate_version():
#     result = 1
#     try:

#         output = generate_version.main()
#         logger.debug(f'_generate_version() type(output) = {type(output)}')
#         logger.debug(f'_generate_version() output = {output}')

#         dict = json.loads(output)

#         if "exit_code" in dict:
#             result = dict["exit_code"]

#         result = dict

#     except ValueError as ve:
#         logger.error(f'output is not json. result = 1', exc_info=ve)
#         return result

#     return result


def _parse_files(i):
    time.sleep(10)
    return i

# [END python functions]

if __name__ == "__main__":
    _generate_version()