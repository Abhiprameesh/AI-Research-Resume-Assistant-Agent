from fastapi import FastAPI
from pydantic import BaseModel

from langchain_core.messages import (
    HumanMessage,
    ToolMessage
)

from agent import llm_with_tools, tools
from memory import chat_history

app = FastAPI()

class UserInput(BaseModel):
    message: str
    resume_path: str | None = None

@app.post("/chat")
def chat(user_input: UserInput):

    # Resume upload handling
    if user_input.resume_path:

        from tools import analyze_resume

        resume_text = analyze_resume.invoke(
            {"file_path": user_input.resume_path}
        )

        chat_history.append(
            HumanMessage(
                content=f"""
                Resume Content:

                {resume_text}

                User Question:
                {user_input.message}
                """
            )
        )

    else:

        chat_history.append(
            HumanMessage(content=user_input.message)
        )

    try:

        response = llm_with_tools.invoke(chat_history)

    except Exception as e:

        return {
            "response": f"Error: {str(e)}"
        }

    chat_history.append(response)

    # Tool calling
    if response.tool_calls:

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            selected_tool = next(
                tool for tool in tools
                if tool.name == tool_name
            )

            tool_result = selected_tool.invoke(
                tool_call["args"]
            )

            tool_message = ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )

            chat_history.append(tool_message)

        final_response = llm_with_tools.invoke(chat_history)

        chat_history.append(final_response)

        if isinstance(final_response.content, list):
            response_text = final_response.content[0]["text"]
        else:
            response_text = final_response.content

        return {
    "response": response_text
}

    if isinstance(response.content, list):
        response_text = response.content[0]["text"]
    else:
        response_text = response.content

    return {
        "response": response_text
    }
