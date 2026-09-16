from sqlalchemy import text

from ai_data_analyst.database.connection import engine
from ai_data_analyst.tools.sql_validator import validate_sql


def execute_sql(sql: str):
    """
    Validate and execute a read-only SQL query.
    """

    is_valid, message = validate_sql(sql)

    if not is_valid:
        raise ValueError(f"SQL validation failed: {message}")

    with engine.connect() as connection:
        result = connection.execute(text(sql))

        columns = list(result.keys())
        rows = [dict(row._mapping) for row in result]

    return {
        "columns": columns,
        "rows": rows,
    }