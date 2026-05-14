from agent import llm

from research_agent import (
    retrieve_research_context
)

def research_agent(user_input):

    research_context = ""

    try:

        chunks = retrieve_research_context(
            user_input
        )

        research_context = "\n".join(
            chunks
        )

    except:

        research_context = ""

    response = llm.invoke(
        f"""
        You are an AI Research Assistant.

        Research Context:
        {research_context}

        User Request:
        {user_input}

        Responsibilities:
        - summarize papers
        - explain methodologies
        - explain architectures
        - simplify concepts
        - explain findings
        - answer research questions

        Give detailed research-focused answers.
        """
    )

    return response.content