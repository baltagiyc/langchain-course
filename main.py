from dotenv import load_dotenv
import os

load_dotenv()
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

llm = ChatOpenAI(model="gpt-5", temperature=0)
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools)

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
