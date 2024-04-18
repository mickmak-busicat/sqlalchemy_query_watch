import logging
import traceback
from typing import Optional
from logging import Logger
from sqlalchemy import event, Engine

from .statement_count_log import reset_statement_count, record_query
from .query_time_log import query_start, query_end_with_time_used
from .check_consecutive_query import add_consecutive_query_count

default_logger = logging.getLogger("sqlalchemy_query_watch")


def sqlalchemy_query_watch(
    db_engine: Engine,
    query_logger: Logger = default_logger,
    query_count_threshold_escalate_log: Optional[int] = 10,
    query_time_too_long_error_second: Optional[int] = 3,
    consecutive_query_count_warning: Optional[int] = 10,
):
    def _receive_checkout(dbapi_connection, conn, connection_proxy):
        query_logger.info(f"conn({hex(id(conn))}) start:")
        conn.info["conn_session"] = hex(id(conn))
        reset_statement_count(conn.info)

    def _receive_before_cursor_execute(
        conn, cursor, statement: str, parameters, context, executemany
    ):
        query_start(conn.info)
        record_query(conn.info, statement=statement)
        query_logger.debug(
            f"conn({conn.info['conn_session']}) "
            f"query: {statement} params: {parameters}"
        )

    def _receive_after_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        total = query_end_with_time_used(conn.info)

        query_length = len(statement)
        param_count = len(parameters)

        add_consecutive_query_count(conn.info, statement, parameters)

        if conn.info.get("same_query_count", 0) > consecutive_query_count_warning:
            query_logger.warning(
                f"conn({conn.info['conn_session']}) "
                f"{conn.info.get('same_query_count')} same consecutive queries detected (Beware of n+1): "
                f"{statement}, {parameters}, ()"
            )
            traceback.print_stack()

        if total > query_time_too_long_error_second:
            query_logger.error(
                f"conn({conn.info['conn_session']}) "
                f"query used too long: {total} "
                f"(query len: {query_length}, param count: {param_count})"
            )
        else:
            query_logger.info(
                f"conn({conn.info['conn_session']}) "
                f"query({conn.info.get('event_count', 0)}) used: {total} "
                f"(query len: {query_length}, param count: {param_count})"
            )

    def _receive_checkin(dbapi_connection, conn):
        result = (
            f"conn({conn.info['conn_session']}) "
            f"end(stmt:{conn.info.get('total')}, io:{conn.info.get('event_count')}):"
        )

        if conn.info.get("select_count", 0) > 0:
            result = f"{result} select({conn.info.get('select_count')})"
        if conn.info.get("update_count", 0) > 0:
            result = f"{result} update({conn.info.get('update_count')})"
        if conn.info.get("insert_count", 0) > 0:
            result = f"{result} insert({conn.info.get('insert_count')})"
        if conn.info.get("delete_count", 0) > 0:
            result = f"{result} delete({conn.info.get('delete_count')})"

        if conn.info.get("total") > query_count_threshold_escalate_log:
            query_logger.warning(result)
        else:
            query_logger.info(result)

    if db_engine is not None:
        event.listen(db_engine, "before_cursor_execute", _receive_before_cursor_execute)
        event.listen(db_engine, "after_cursor_execute", _receive_after_cursor_execute)
        event.listen(db_engine, "checkout", _receive_checkout)
        event.listen(db_engine, "checkin", _receive_checkin)
