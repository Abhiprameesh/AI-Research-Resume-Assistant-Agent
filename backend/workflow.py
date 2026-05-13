from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    END
)

import json

from tools import web_search

from agent import llm

from research_agent import (
    retrieve_research_context
)

# STATE
class AgentState(TypedDict):

    user_input: str
    resume_text: str
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
def executor_node(state: AgentState):

    user_input = state["user_input"]

    resume_text = state.get(
        "resume_text",
        ""
    )

    plan = state["plan"]

    # Parse planner output
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

    # Web Search
    search_result = ""

    if "web_search" in tools_needed:

        try:

            search_result = web_search.invoke(
                {"query": user_input}
            )

        except:

            search_result = ""

    # Research Paper Retrieval
    research_context = ""

    try:

        research_chunks = retrieve_research_context(
            user_input
        )

        research_context = "\n".join(
            research_chunks
        )

    except:

        research_context = ""

    # Final LLM Response
    response = llm.invoke(
        f"""
        User Request:
        {user_input}

        Resume Context:
        {resume_text}

        Research Paper Context:
        {research_context}

        Execution Plan:
        {plan}

        Search Results:
        {search_result}

        Use the Research Paper Context heavily
        when answering research-related questions.

        If research context exists:
        - summarize the paper
        - explain methodology
        - explain architecture
        - explain findings clearly

        If resume context exists:
        - analyze the resume properly
        - give ATS suggestions
        - suggest improvements

        Generate a detailed helpful response.
        """
    )

    return {
        "response": response.content
    }


# BUILD GRAPH
graph = StateGraph(AgentState)

# ADD NODES
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