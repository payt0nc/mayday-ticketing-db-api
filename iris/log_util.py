import json
from datetime import datetime


def get_log_msg(endpoint, process_time, request, response):
    return json.dumps(
        dict(
            endpoint=endpoint,
            ts=int(datetime.utcnow().timestamp()),
            process_time=process_time,
            request=request,
            response=response),
        ensure_ascii=False,
        sort_keys=True)
