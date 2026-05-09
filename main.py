from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = llm.invoke(user_input)

    print("\nAgent:", response.content)