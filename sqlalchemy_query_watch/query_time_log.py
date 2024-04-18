import time


def query_start(conn_info: dict):
    conn_info.setdefault("query_start_time", []).append(time.time())


def query_end_with_time_used(conn_info: dict):
    return time.time() - conn_info["query_start_time"].pop(-1)
