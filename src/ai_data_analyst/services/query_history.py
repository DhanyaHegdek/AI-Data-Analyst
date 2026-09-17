from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from ai_data_analyst.database.connection import engine
from ai_data_analyst.models.query import Query


def save_query(
    question: str,
    generated_sql: str | None,
) -> Query:
    """Save an analyzed question and its generated SQL."""

    with Session(engine) as session:
        query = Query(
            question=question,
            generated_sql=generated_sql,
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