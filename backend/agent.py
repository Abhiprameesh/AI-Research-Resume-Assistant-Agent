from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from tools import (
    get_current_time,
    motivational_quote,
    resume_tip,
    generate_ml_interview_question,
    web_search,
    analyze_resume
    
)

load_dotenv()

tools = [
    get_current_time,
    motivational_quote,
    resume_tip,
    generate_ml_interview_question,
    web_search,
    analyze_resume
]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

llm_with_tools = llm.bind_tools(tools)