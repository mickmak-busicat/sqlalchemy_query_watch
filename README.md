# sqlalchemy_query_watch
Additional query log for SqlAlchemy

- Query summary within a db connection
  - Statement count (`SELECT`, `UPDATE`, `INSERT`, `DELETE`)
  - DB IO count
    - Turn to `WARNING` log level when too many IO count within a connection
- Time used on every query
  - Turn to `ERROR` log level when query takes too long to execute
- Raw query (`DEBUG` log level)
- Query length and parameter on every query (with n+1 detection using this stats)
