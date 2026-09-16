from ai_data_analyst.services.gemini import llm


SQL_FIX_PROMPT = """
You are an expert PostgreSQL SQL developer.

The generated SQL failed validation.

Fix the SQL so that it is safe and valid.

USER QUESTION:
{question}

DATABASE SCHEMA:
{schema}

INVALID SQL:
{sql}

VALIDATION ERROR:
{validation_message}

RULES:
1. Return ONLY the corrected SQL.
2. Use PostgreSQL syntax.
3. Only generate SELECT queries.
4. Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, or other DDL/DML.
5. Use only tables and columns present in the schema.
6. Preserve the original user's intent.
7. Do not add markdown.
"""


def fix_sql(state: dict) -> dict:
    question = state["question"]
    schema = state["schema"]
    sql = state["sql"]
    validation_message = state.get(
        "validation_message",
        "SQL validation failed.",
    )

    prompt = SQL_FIX_PROMPT.format(
        question=question,
        schema=schema,
        sql=sql,
        validation_message=validation_message,
    )

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, str):
        fixed_sql = content.strip()

    elif isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, str):
                text_parts.append(block)

            elif isinstance(block, dict):
                text = block.get("text")

                if text:
                    text_parts.append(text)

        fixed_sql = "".join(text_parts).strip()

    else:
        raise TypeError(
            f"Unexpected Gemini response content type: {type(content)}"
        )

    if fixed_sql.startswith("```"):
        fixed_sql = fixed_sql.strip("`")

        if fixed_sql.startswith("sql"):
            fixed_sql = fixed_sql[3:].strip()

    retry_count = state.get("retry_count", 0) + 1

    return {
        "sql": fixed_sql,
        "retry_count": retry_count,
    }