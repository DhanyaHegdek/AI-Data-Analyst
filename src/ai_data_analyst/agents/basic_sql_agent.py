from ai_data_analyst.agents.sql_generator import generate_sql
from ai_data_analyst.services.sql_executor import execute_sql


def run_basic_sql_agent(question: str) -> dict:
    """
    Convert a natural-language question into SQL,
    validate it, execute it, and return the result.
    """

    # 1. Generate SQL using Gemini
    sql = generate_sql(question)

    # 2. Validate + execute SQL
    result = execute_sql(sql)

    # 3. Return everything needed downstream
    return {
        "question": question,
        "sql": sql,
        "columns": result["columns"],
        "rows": result["rows"],
    }