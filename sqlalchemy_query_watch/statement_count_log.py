def reset_statement_count(conn_info: dict):
    conn_info["select_count"] = 0
    conn_info["update_count"] = 0
    conn_info["insert_count"] = 0
    conn_info["delete_count"] = 0
    conn_info["event_count"] = 0
    conn_info["total"] = 0


def record_query(conn_info: dict, statement: str):
    select_count = statement.count("SELECT ")
    update_count = statement.count("UPDATE ")
    insert_count = statement.count("INSERT ")
    delete_count = statement.count("DELETE ")

    conn_info["event_count"] = conn_info.get("event_count", 0) + 1
    conn_info["select_count"] = conn_info.get("select_count", 0) + select_count
    conn_info["update_count"] = conn_info.get("update_count", 0) + update_count
    conn_info["insert_count"] = conn_info.get("insert_count", 0) + insert_count
    conn_info["delete_count"] = conn_info.get("delete_count", 0) + delete_count
    conn_info["total"] = (
        conn_info.get("total", 0)
        + select_count
        + update_count
        + insert_count
        + delete_count
    )
