from fastapi import FastAPI
from pydantic import BaseModel

from workflow import app_workflow

from vector_memory import (
    store_memory,
    retrieve_memory
)

from profile_memory import (
    save_profile,
    load_profile
)

app = FastAPI()

# INPUT MODEL
class UserInput(BaseModel):

    message: str
    resume_path: str | None = None

# CHAT ENDPOINT
@app.post("/chat")
def chat(user_input: UserInput):

    try:

        # Load persistent user profile
        profile_data = load_profile()

        # Retrieve semantic memories
        relevant_memories = retrieve_memory(
            user_input.message
        )

        memory_context = "\n".join(
            relevant_memories
        )

        memory_context = f"""
        These are important memories from previous conversations:

        {memory_context}

        Use them only if relevant.
        """

        # Resume handling
        resume_text = ""

        if user_input.resume_path:

            from tools import analyze_resume

            resume_text = analyze_resume.invoke(
                {
                    "file_path": user_input.resume_path
                }
            )

            # Update persistent profile
            profile_data["resume_uploaded"] = True

            profile_data["career_interest"] = (
                "AI Research Internships"
            )

            save_profile(profile_data)

        # Run LangGraph workflow
        workflow_result = app_workflow.invoke(
            {
                "user_input": f"""
                User Profile:
                {profile_data}

                Previous Relevant Memories:
                {memory_context}

                Current User Message:
                {user_input.message}
                """,

                "resume_text": resume_text
            }
        )

        response_text = workflow_result["response"]

        # Store important semantic memory
        important_memory = f"""
        User Query:
        {user_input.message}

        AI Response:
        {response_text}
        """

        store_memory(important_memory)

        return {
            "response": response_text
        }

    except Exception as e:

        return {
            "response": f"Error: {str(e)}"
        }