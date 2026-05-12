from typing import TypedDict

from langgraph.graph import StateGraph, END

from tools import web_search

from agent import llm

# STATE
class AgentState(TypedDict):

    user_input: str
    plan: str
    response: str

# PLANNER NODE
def planner_node(state: AgentState):

    user_input = state["user_input"]

    response = llm.invoke(
        f"""
        You are an AI planner.

        Analyze the user request and return ONLY valid JSON.

        JSON format:

        {{
            "goal": "...",
            "steps": [
                "...",
                "..."
            ],
            "tools_needed": [
                "...",
                "..."
            ]
        }}

        User Request:
        {user_input}
        """
    )

    return {
        "plan": response.content
    }

# EXECUTOR NODE
import json

def executor_node(state: AgentState):

    user_input = state["user_input"]

    plan = state["plan"]

    try:

        parsed_plan = json.loads(plan)

    except:

        parsed_plan = {
            "goal": user_input,
            "steps": [],
            "tools_needed": []
        }

    tools_needed = parsed_plan.get(
        "tools_needed",
        []
    )

    search_result = ""

    # Use web search if needed
    if "web_search" in tools_needed:

        search_result = web_search.invoke(
            {"query": user_input}
        )

    response = llm.invoke(
        f"""
        User Request:
        {user_input}

        Execution Plan:
        {parsed_plan}

        Search Results:
        {search_result}

        Generate a final helpful response.
        """
    )

    return {
        "response": response.content
    }
# BUILD GRAPH
graph = StateGraph(AgentState)

# NODES
graph.add_node(
    "planner",
    planner_node
)

graph.add_node(
    "executor",
    executor_node
)

# FLOW
graph.set_entry_point("planner")

graph.add_edge(
    "planner",
    "executor"
)

graph.add_edge(
    "executor",
    END
)

# COMPILE
app_workflow = graph.compile()