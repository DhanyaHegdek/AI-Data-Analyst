import json

from ai_data_analyst.services.gemini import llm


QUESTION_UNDERSTANDING_PROMPT = """
You are a data analyst assistant.

Analyze the user's business question and return ONLY valid JSON.

Identify:

- intent: the main analytical task
- metric: the business metric being requested
- dimension: what the metric is grouped or analyzed by
- filters: important conditions from the question
- time_range: requested time period

Return exactly this JSON structure:

{{
    "intent": "...",
    "metric": "...",
    "dimension": "...",
    "filters": [],
    "time_range": "..."
}}

Do not generate SQL.
Do not use markdown.
Do not add explanations.

USER QUESTION:
{question}
"""


def understand_question(state: dict) -> dict:
    question = state["question"]

    prompt = QUESTION_UNDERSTANDING_PROMPT.format(
        question=question
    )

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, str):
                text_parts.append(block)
            elif isinstance(block, dict):
                text = block.get("text")
                if text:
                    text_parts.append(text)

        content = "".join(text_parts)

    content = content.strip()

    # Remove accidental markdown fences if Gemini adds them.
    if content.startswith("```"):
        content = content.strip("`")

        if content.startswith("json"):
            content = content[4:].strip()

    parsed = json.loads(content)

    return {
        "intent": parsed["intent"],
        "metric": parsed["metric"],
        "dimension": parsed["dimension"],
        "filters": parsed["filters"],
        "time_range": parsed["time_range"],
    }