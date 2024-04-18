def add_consecutive_query_count(conn_info: dict, statement: str, parameters: str):
    query_length = len(statement)
    param_count = len(parameters)

    if (
        conn_info.get("last_query_length", None) == query_length
        and conn_info.get("last_param_count", None) == param_count
    ):
        conn_info["same_query_count"] = conn_info.get("same_query_count", 0) + 1
    else:
        conn_info["last_query_length"] = query_length
        conn_info["last_param_count"] = param_count
        conn_info["same_query_count"] = 1
