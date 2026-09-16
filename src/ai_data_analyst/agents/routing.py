def validation_router(state: dict) -> str:
    """
    Decide what happens after SQL validation.
    """

    if state.get("is_valid"):
        return "execute_sql"

    return "fix_sql"