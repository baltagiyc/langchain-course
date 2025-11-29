import os

from dotenv import load_dotenv

load_dotenv()

from langchain import hub
from langchain.agents import AgentExecutor, create_agent, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch


def main():
    print("Hello from langchain-course!")


agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)

if __name__ == "__main__":
    main()
