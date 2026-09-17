from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from decimal import Decimal
from ai_data_analyst.database.connection import engine
from ai_data_analyst.models.query import Query


def save_query(
    question: str,
    generated_sql: str | None,
    result_rows: list | None = None,
    analysis: str | None = None,
    visualization: dict | None = None,
    final_response: str | None = None,
) -> Query:
    """Save an analyzed question and its generated SQL."""

    with Session(engine) as session:
        query = Query(
            question=question,
            generated_sql=generated_sql,
            result_rows=make_json_safe(result_rows),
            analysis=analysis,
            visualization=visualization,
            final_response=final_response,
        )

        session.add(query)
        session.commit()
        session.refresh(query)

        return query


def get_query_history(limit: int = 50) -> list[Query]:
    """Return recent queries, newest first."""

    with Session(engine) as session:
        statement = (
            select(Query)
            .order_by(desc(Query.created_at))
            .limit(limit)
        )

        return list(session.scalars(statement).all())

    
def make_json_safe(value):
    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, list):
        return [make_json_safe(item) for item in value]

    if isinstance(value, dict):
        return {key: make_json_safe(item) for key, item in value.items()}

    return value