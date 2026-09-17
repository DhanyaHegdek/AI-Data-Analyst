from datetime import datetime, timezone

from sqlalchemy import DateTime, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column

from ai_data_analyst.database.base import Base


class Query(Base):
    __tablename__ = "queries"

    id: Mapped[int] = mapped_column(primary_key=True)

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    generated_sql: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    result_rows: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    analysis: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    visualization: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    final_response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )