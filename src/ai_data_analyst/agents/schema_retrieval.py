from ai_data_analyst.agents.schema_context import BUSINESS_SCHEMA


def retrieve_schema(state: dict) -> dict:
    """
    Retrieve database schema context for the current question.

    For the initial implementation, we provide the complete
    business schema. Later this can be replaced with intelligent
    table selection.
    """

    return {
        "schema": BUSINESS_SCHEMA
    }