from ai_data_analyst.services.gemini import llm


FINAL_RESPONSE_PROMPT = """
You are an AI business data analyst.

Create the final answer to the user's question.

USER QUESTION:
{question}

ANALYSIS:
{analysis}

VISUALIZATION:
{visualization}

QUERY RESULTS:
{rows}

Rules:
1. Answer the user's question directly.
2. Use only facts supported by the analysis and query results.
3. Keep the answer concise and business-friendly.
4. Mention important numbers when relevant.
5. Do not mention Gemini, SQL, PostgreSQL, LangGraph, or internal implementation.
6. Do not invent information.
"""


def create_final_response(state: dict) -> dict:
    prompt = FINAL_RESPONSE_PROMPT.format(
        question=state["question"],
        analysis=state.get("analysis", ""),
        visualization=state.get("visualization", {}),
        rows=state.get("rows", []),
    )

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, str):
        final_response = content.strip()

    elif isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, str):
                text_parts.append(block)

            elif isinstance(block, dict):
                text = block.get("text")

                if text:
                    text_parts.append(text)

        final_response = "".join(text_parts).strip()

    else:
        raise TypeError(
            f"Unexpected Gemini response content type: {type(content)}"
        )

    return {
        "final_response": final_response
    }