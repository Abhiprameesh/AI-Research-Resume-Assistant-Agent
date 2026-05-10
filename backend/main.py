from dotenv import load_dotenv
import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.messages import SystemMessage

load_dotenv()

# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# TOOL 1
@tool
def get_current_time() -> str:
    """Returns the current date and time."""
    return str(datetime.datetime.now())

# TOOL 2
@tool
def motivational_quote() -> str:
    """Returns a motivational quote."""
    return "Success comes from consistency and discipline."

@tool
def resume_tip() -> str:
    """Returns a resume improvement tip."""
    return "Use action verbs and measurable achievements in resume bullet points."

@tool
def generate_ml_interview_question() -> str:
    """Returns an AI/ML interview question."""
    return "Explain the difference between supervised and unsupervised learning."

# Bind tools
tools = [
    get_current_time,
    motivational_quote,
    resume_tip,
    generate_ml_interview_question
]
llm_with_tools = llm.bind_tools(tools)

chat_history = [
    SystemMessage(
        content="""
        You are a helpful AI assistant.

        You must remember previous conversation context
        and answer based on chat history whenever relevant.
        """
    )
]

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # Add user message to memory
    chat_history.append(HumanMessage(content=user_input))

    # Invoke model
    response = llm_with_tools.invoke(chat_history)

    # Add AI response
    chat_history.append(response)

    # Tool calling
    if response.tool_calls:

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            selected_tool = next(
                tool for tool in tools if tool.name == tool_name
            )

            tool_result = selected_tool.invoke(tool_call["args"])

            tool_message = ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )

            chat_history.append(tool_message)

        final_response = llm_with_tools.invoke(chat_history)

        chat_history.append(final_response)

        print("\nAgent:", final_response.content)

    else:
        print("\nAgent:", response.content)