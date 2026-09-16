def validation_router(state: dict) -> str:
    """
    Decide what happens after SQL validation.
    """

    if state.get("is_valid"):
        return "execute_sql"

    retry_count = state.get("retry_count", 0)

    if retry_count >= 2:
        return "final_response"

    return "fix_sql"