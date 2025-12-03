from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_classic.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_classic.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

@tool
def multiplicator(x: int, y: int) -> int:
    """Multiply 'x' times 'y'."""
    return x * y

def main():
    print("Hello in tool-calling from langchain-course!")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "you are a helpful assistant"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    tools = [multiplicator, TavilySearchResults()]

    llm = ChatOpenAI(model="gpt-5", temperature=0)

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    resultat=agent_executor.invoke({"input": "C'est quoi le prochain gros évènement DATA / IA à Paris à venir ? Calcule moi le produit de 10 par 20"})

    print(resultat)

if __name__ == "__main__":
    main()
