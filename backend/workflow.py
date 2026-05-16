from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    END
)

from agent import llm

# AGENTS
from agents.router_agent import (
    router_agent
)

from agents.resume_agent import (
    resume_agent
)

from agents.research_agent_node import (
    research_agent
)

from agents.career_agent import (
    career_agent
)

from agents.interview_agent import (
    interview_agent
)

# STATE
class AgentState(TypedDict):

    user_input: str
    resume_text: str
    response: str

    selected_agent: str
    retrieved_memories: list
    retrieved_chunks: list


# PLANNER NODE
def planner_node(state: AgentState):

    user_input = state["user_input"]

    response = llm.invoke(
        f"""
        You are an AI planner.

        Understand the user's request carefully.

        Briefly analyze:
        - what the user wants
        - what type of task it is
        - which specialized agent may help

        User Request:
        {user_input}
        """
    )

    return {
        "response": response.content
    }


# EXECUTOR NODE
def executor_node(state: AgentState):

    user_input = state["user_input"]

    resume_text = state.get(
        "resume_text",
        ""
    )

    # ROUTER DECISION
    selected_agent = router_agent(
        user_input
    )

    # OBSERVABILITY VARIABLES
    retrieved_memories = []

    retrieved_chunks = []

    # RESUME AGENT
    if "resume" in selected_agent:

        response = resume_agent(
            user_input,
            resume_text
        )

    # RESEARCH AGENT
    elif "research" in selected_agent:

        response, retrieved_chunks = research_agent(
            user_input,
            return_chunks=True
        )

    # INTERVIEW AGENT
    elif "interview" in selected_agent:

        response = interview_agent(
            user_input
        )

    # DEFAULT → CAREER AGENT
    else:

        response = career_agent(
            user_input
        )

    return {
        "response": response,
        "selected_agent": selected_agent,
        "retrieved_memories": retrieved_memories,
        "retrieved_chunks": retrieved_chunks
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