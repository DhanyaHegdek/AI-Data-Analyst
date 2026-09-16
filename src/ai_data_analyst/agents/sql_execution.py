from ai_data_analyst.services.sql_executor import execute_sql


def execute_sql_node(state: dict) -> dict:
    """
    Execute validated SQL and store the results in the agent state.
    """

    if not state.get("is_valid"):
        return {
            "error": "SQL execution skipped because validation failed."
        }

    try:
        result = execute_sql(state["sql"])

        return {
            "columns": result["columns"],
            "rows": result["rows"],
        }

    except Exception as exc:
        return {
            "error": str(exc)
        }