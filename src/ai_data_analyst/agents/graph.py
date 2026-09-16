from langgraph.graph import END, START, StateGraph

from ai_data_analyst.agents.final_response import create_final_response
from ai_data_analyst.agents.question_understanding import understand_question
from ai_data_analyst.agents.result_analysis import analyze_results
from ai_data_analyst.agents.schema_retrieval import retrieve_schema
from ai_data_analyst.agents.sql_execution import execute_sql_node
from ai_data_analyst.agents.sql_generator import generate_sql
from ai_data_analyst.agents.sql_validation import validate_sql_node
from ai_data_analyst.agents.state import AnalystState
from ai_data_analyst.agents.visualization import select_visualization


def build_graph():
    graph = StateGraph(AnalystState)

    graph.add_node("understand_question", understand_question)
    graph.add_node("retrieve_schema", retrieve_schema)
    graph.add_node("generate_sql", generate_sql)
    graph.add_node("validate_sql", validate_sql_node)
    graph.add_node("execute_sql", execute_sql_node)
    graph.add_node("analyze_results", analyze_results)
    graph.add_node("select_visualization", select_visualization)
    graph.add_node("final_response", create_final_response)

    graph.add_edge(START, "understand_question")
    graph.add_edge("understand_question", "retrieve_schema")
    graph.add_edge("retrieve_schema", "generate_sql")
    graph.add_edge("generate_sql", "validate_sql")
    graph.add_edge("validate_sql", "execute_sql")
    graph.add_edge("execute_sql", "analyze_results")
    graph.add_edge("analyze_results", "select_visualization")
    graph.add_edge("select_visualization", "final_response")
    graph.add_edge("final_response", END)

    return graph.compile()


analyst_graph = build_graph()