from ai_data_analyst.agents.schema_context import BUSINESS_SCHEMA
from ai_data_analyst.services.gemini import llm


SQL_GENERATION_PROMPT = """
You are an expert PostgreSQL data analyst.

Your task is to convert a user's natural-language business
question into a valid PostgreSQL SELECT query.

You have access only to the database schema provided below.

DATABASE SCHEMA:
{schema}

RULES:
1. Generate only a SELECT query.
2. Never generate INSERT, UPDATE, DELETE, DROP, ALTER,
   CREATE, TRUNCATE, or other write/DDL statements.
3. Use only tables and columns that exist in the schema.
4. Use correct JOIN conditions based on the relationships.
5. For revenue calculations, use:
   quantity * unit_price
   from order_items unless the question specifically
   requires another field.
6. Use PostgreSQL syntax.
7. Return ONLY the SQL query.
8. Do not use markdown code fences.
9. Do not explain the query.

USER QUESTION:
{question}
"""


def generate_sql(question: str) -> str:
    prompt = SQL_GENERATION_PROMPT.format(
        schema=BUSINESS_SCHEMA,
        question=question,
    )

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, str):
        sql = content.strip()

    elif isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, str):
                text_parts.append(block)

            elif isinstance(block, dict):
                text = block.get("text")

                if text:
                    text_parts.append(text)

        sql = "".join(text_parts).strip()

    else:
        raise TypeError(
            f"Unexpected Gemini response content type: {type(content)}"
        )

    return sql