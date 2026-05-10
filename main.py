from dotenv import load_dotenv
import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

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

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # First response from model
    response = llm_with_tools.invoke([HumanMessage(content=user_input)])

    # If model wants to use tools
    if response.tool_calls:

        messages = [HumanMessage(content=user_input), response]

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            # Find matching tool
            selected_tool = next(
                tool for tool in tools if tool.name == tool_name
            )

            # Execute tool
            tool_result = selected_tool.invoke(tool_call["args"])

            # Add tool result
            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )
            )

        # Final AI response
        final_response = llm_with_tools.invoke(messages)

        print("\nAgent:", final_response.content)

    else:
        print("\nAgent:", response.content)