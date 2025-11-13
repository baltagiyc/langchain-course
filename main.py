from dotenv import load_dotenv
import os

load_dotenv()
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

@tool
def search(query:str) -> str:
    """
    Search the web for information
    Args:
        query: The query to search for
    Returns:
        The search results
    """
    print(f"Searching the web for {query}")
    return tavily.search(query)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [search]
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
