from ai_data_analyst.services.gemini import llm


VISUALIZATION_PROMPT = """
You are a data visualization expert.

Based on the user's question and query results, decide the
most appropriate visualization.

USER QUESTION:
{question}

QUERY RESULTS:
{results}

Return ONLY valid JSON:

{{
    "chart_type": "bar|line|pie|table",
    "x_axis": "...",
    "y_axis": "...",
    "title": "..."
}}

Rules:
1. Use "bar" for rankings or category comparisons.
2. Use "line" for trends over time.
3. Use "pie" only for simple proportions/distributions.
4. Use "table" when a chart would not add meaningful value.
5. Do not invent columns.
6. Use column names that actually exist in the results.
7. Do not use markdown.
"""


def select_visualization(state: dict) -> dict:
    question = state["question"]
    rows = state.get("rows", [])

    prompt = VISUALIZATION_PROMPT.format(
        question=question,
        results=rows,
    )

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, str):
        text = content.strip()

    elif isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, str):
                text_parts.append(block)

            elif isinstance(block, dict):
                block_text = block.get("text")

                if block_text:
                    text_parts.append(block_text)

        text = "".join(text_parts).strip()

    else:
        raise TypeError(
            f"Unexpected Gemini response content type: {type(content)}"
        )

    if text.startswith("```"):
        text = text.strip("`")

        if text.startswith("json"):
            text = text[4:].strip()

    import json

    visualization = json.loads(text)

    return {
        "visualization": visualization
    }