from agent import llm

def resume_agent(
    user_input,
    resume_text
):

    response = llm.invoke(
        f"""
        You are an expert AI Resume Reviewer.

        Resume:
        {resume_text}

        User Request:
        {user_input}

        Responsibilities:
        - ATS analysis
        - strengths/weaknesses
        - missing skills
        - project suggestions
        - formatting advice
        - career improvement advice

        Give detailed professional feedback.
        """
    )

    return response.content