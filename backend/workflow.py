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

    plan = llm.invoke(
        f"""
        You are an AI planner.

        Break the user's request into logical steps.

        User Request:
        {user_input}

        Create a short execution plan.
        """
    )

    return {
        "plan": plan.content
    }

# EXECUTOR NODE
def executor_node(state: AgentState):

    user_input = state["user_input"]

    plan = state["plan"]

    # Decide whether search is needed
    if "latest" in user_input.lower() \
        or "news" in user_input.lower() \
        or "search" in user_input.lower():

        search_result = web_search.invoke(
            {"query": user_input}
        )

        response = llm.invoke(
            f"""
            User Request:
            {user_input}

            Execution Plan:
            {plan}

            Web Search Results:
            {search_result}

            Generate final response.
            """
        )

    else:

        response = llm.invoke(
            f"""
            User Request:
            {user_input}

            Execution Plan:
            {plan}

            Generate final response.
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