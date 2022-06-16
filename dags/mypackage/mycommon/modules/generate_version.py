#!/usr/bin/env python3

# imports
import logging
import json
import time
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mypackage.mycommon.modules.generate_version")

def main():
    result = {
        "exit_code": 1,
        "exit_msg": "Exception",
        "total_processed": 0,
        "total_failed": 0,
        "version": 0,
        "elasped_time": 0,
        "utc": ""
    }

    try:
        start_time = time.perf_counter()

        utc_now = datetime.datetime.utcnow()
        utc_format = utc_now.isoformat()
        version = int(utc_now.replace(tzinfo= datetime.timezone.utc).timestamp())

        # raise ValueError('TEST error in python module')

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        result = {
            "exit_code": 0,
            "exit_msg": "Success",
            "total_processed": 1,
            "total_failed": 0,
            "version": version,
            "elasped_time": elapsed_time,
            "utc": utc_format
        }


    except Exception as e:
        logger.exception("Unhandled Exception", exc_info=e)

    finally:
        return json.dumps(result)


if __name__ == "__main__":
    print(main())