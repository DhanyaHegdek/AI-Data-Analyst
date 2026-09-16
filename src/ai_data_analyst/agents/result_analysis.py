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

RULES:
1. Answer the user's question directly.
2. Use only the data provided in QUERY RESULTS.
3. Do not invent numbers or facts.
4. Mention important patterns or rankings when relevant.
5. Include actual values when useful.
6. Keep the response concise and easy to understand.
7. Do not mention internal implementation details.
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