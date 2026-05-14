from agent import llm

def interview_agent(user_input):

    response = llm.invoke(
        f"""
        You are an AI Mock Interviewer.

        User Request:
        {user_input}

        Responsibilities:
        - ask ML interview questions
        - ask HR questions
        - evaluate answers
        - provide interview feedback
        - test AI/ML concepts

        Conduct professional interviews.
        """
    )

    return response.content