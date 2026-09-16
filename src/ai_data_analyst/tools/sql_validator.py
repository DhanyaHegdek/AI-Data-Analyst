from sqlglot import exp, parse_one


FORBIDDEN_EXPRESSIONS = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Create,
    exp.Alter,
    exp.Drop,
    exp.TruncateTable,
)


def validate_sql(sql: str) -> tuple[bool, str]:
    """
    Validate AI-generated SQL before database execution.

    Returns:
        (True, "SQL is valid") when safe.
        (False, reason) when rejected.
    """

    if not sql or not sql.strip():
        return False, "SQL query is empty."

    sql = sql.strip()

    # --------------------------------------------------
    # Only allow one SQL statement
    # --------------------------------------------------

    statements = sql.split(";")

    non_empty_statements = [
        statement.strip()
        for statement in statements
        if statement.strip()
    ]

    if len(non_empty_statements) > 1:
        return False, "Multiple SQL statements are not allowed."

    # --------------------------------------------------
    # Parse PostgreSQL SQL
    # --------------------------------------------------

    try:
        tree = parse_one(sql, read="postgres")
    except Exception as exc:
        return False, f"Invalid SQL syntax: {exc}"

    # --------------------------------------------------
    # Block dangerous operations
    # --------------------------------------------------

    for forbidden_expression in FORBIDDEN_EXPRESSIONS:
        if tree.find(forbidden_expression):
            return (
                False,
                f"Forbidden SQL operation: "
                f"{forbidden_expression.__name__}",
            )

    # --------------------------------------------------
    # Only SELECT statements are allowed
    # --------------------------------------------------

    if not isinstance(tree, exp.Select):
        return False, "Only SELECT queries are allowed."

    return True, "SQL is valid."