from agent import llm

def career_agent(user_input):

    response = llm.invoke(
        f"""
        You are an AI Career Mentor.

        User Request:
        {user_input}

        Responsibilities:
        - AI/ML career guidance
        - internship advice
        - roadmap creation
        - learning strategies
        - skill recommendations
        - project guidance

        Give practical career advice.
        """
    )

    return response.content