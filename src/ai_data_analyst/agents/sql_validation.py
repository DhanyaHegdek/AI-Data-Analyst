from ai_data_analyst.tools.sql_validator import validate_sql


def validate_sql_node(state: dict) -> dict:
    sql = state["sql"]

    is_valid, message = validate_sql(sql)

    return {
        "is_valid": is_valid,
        "validation_message": message,
    }