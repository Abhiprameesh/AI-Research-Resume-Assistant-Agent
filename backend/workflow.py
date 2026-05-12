from typing import TypedDict

from langgraph.graph import StateGraph, END

from tools import (
    web_search,
    analyze_resume
)

from agent import llm

# STATE
class AgentState(TypedDict):

    user_input: str
    response: str

# ROUTER NODE
def router(state: AgentState):

    user_input = state["user_input"].lower()

    if "resume" in user_input:
        return "resume"

    elif "search" in user_input \
        or "latest" in user_input \
        or "news" in user_input:

        return "search"

    else:
        return "general"

# RESUME NODE
def resume_node(state: AgentState):

    response = llm.invoke(
        f"""
        Give resume advice for:
        {state['user_input']}
        """
    )

    return {
        "response": response.content
    }

# SEARCH NODE
def search_node(state: AgentState):

    search_result = web_search.invoke(
        {"query": state["user_input"]}
    )

    response = llm.invoke(
        f"""
        Based on this search result:

        {search_result}

        Answer the user query:
        {state['user_input']}
        """
    )

    return {
        "response": response.content
    }

# GENERAL NODE
def general_node(state: AgentState):

    response = llm.invoke(
        state["user_input"]
    )

    return {
        "response": response.content
    }

# BUILD GRAPH
graph = StateGraph(AgentState)

# ADD NODES
graph.add_node("resume", resume_node)

graph.add_node("search", search_node)

graph.add_node("general", general_node)

# ROUTING
graph.set_conditional_entry_point(
    router,
    {
        "resume": "resume",
        "search": "search",
        "general": "general"
    }
)

# END STATES
graph.add_edge("resume", END)

graph.add_edge("search", END)

graph.add_edge("general", END)

# COMPILE
app_workflow = graph.compile()