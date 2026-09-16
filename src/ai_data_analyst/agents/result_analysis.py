from ai_data_analyst.services.gemini import llm


RESULT_ANALYSIS_PROMPT = """
You are a business data analyst.

Analyze the SQL query result and provide a concise,
fact-based business insight.

USER QUESTION:
{question}

SQL QUERY:
{sql}

QUERY RESULTS:
{results}

Rules:
1. Answer the user's question directly.
2. Use ONLY information explicitly present in QUERY RESULTS.
3. Do not infer product categories, customer segments, locations, trends, or other facts unless they are present in QUERY RESULTS.
4. Do not invent or assume a currency.
5. Do not add currency symbols unless the query results explicitly contain one.
6. Do not invent numbers, percentages, totals, or comparisons.
7. Calculate comparisons only from the provided numeric values.
8. Mention important rankings or patterns only when supported by the results.
9. Include actual values when useful.
10. Keep the response concise and business-friendly.
11. Do not mention Gemini, SQL, PostgreSQL, LangGraph, or internal implementation details.
"""


def analyze_results(state: dict) -> dict:
    question = state["question"]
    sql = state["sql"]
    rows = state.get("rows", [])

    prompt = RESULT_ANALYSIS_PROMPT.format(
        question=question,
        sql=sql,
        results=rows,
    )

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, str):
        analysis = content.strip()

    elif isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, str):
                text_parts.append(block)

            elif isinstance(block, dict):
                text = block.get("text")

                if text:
                    text_parts.append(text)

        analysis = "".join(text_parts).strip()

    else:
        raise TypeError(
            f"Unexpected Gemini response content type: {type(content)}"
        )

    return {
        "analysis": analysis
    }