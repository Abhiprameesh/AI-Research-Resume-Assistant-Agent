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

@app.post("/chat")
def chat(user_input: UserInput):

    chat_history.append(
        HumanMessage(content=user_input.message)
    )

    response = llm_with_tools.invoke(chat_history)

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

        return {
            "response": final_response.content
        }

    return {
        "response": response.content
    }