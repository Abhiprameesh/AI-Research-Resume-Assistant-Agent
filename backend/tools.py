from langchain_core.tools import tool
import datetime

@tool
def get_current_time() -> str:
    """Returns current date and time."""
    return str(datetime.datetime.now())

@tool
def motivational_quote() -> str:
    """Returns motivational quote."""
    return "Success comes from consistency and discipline."

@tool
def resume_tip() -> str:
    """Returns a resume improvement tip."""
    return "Use action verbs and measurable achievements."

@tool
def generate_ml_interview_question() -> str:
    """Returns an ML interview question."""
    return "Explain bias vs variance in machine learning."