from dotenv import load_dotenv
import os

from typing import List
from pydantic import BaseModel, Field
load_dotenv()
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

class Source(BaseModel):
    """Schema for a source used by the agent"""
    url:str = Field(description="The url of the source")

class AgentResponse(BaseModel):
    """Schema for the agent reponse"""
    answer:str = Field(description="The answer to the question")
    sources:List[Source] = Field(default_factory=list, description="The sources used to answer the question")

llm = ChatOpenAI(model="gpt-5", temperature=0)
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)

def main():
    print("Hello from langchain-course!")
    # Vérifier que la clé API est définie
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set!")
        return
    
    # Essayer avec des messages explicites
    from langchain_core.messages import HumanMessage
    result = agent.invoke({
        "messages": [HumanMessage(content="C'est quoi la météo à Istanbul la semaine prochaine ?")]
    })
    print(result)

if __name__ == "__main__":
    main()
