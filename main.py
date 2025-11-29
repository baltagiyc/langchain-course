from dotenv import load_dotenv

load_dotenv()

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool
from pydantic import BaseModel, Field
import os
from tavily import TavilyClient

from typing import List
from schema import Source
from prompt import REACT_PROMPT_WITH_REACT_INSTRUCTIONS

class AgentResponse(BaseModel):
    """Schema for the agent response"""
    answer: str = Field(description="The answer to the question")
    sources: List[Source] = Field(default_factory=list, description="The sources used to answer the question")

# Créer un client Tavily pour l'extraction
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

@tool
def extract_url_content(url: str) -> str:
    """
    Extract the full content from a specific URL.
    Use this when you have a URL and want to read its content.
    Do NOT use this with search queries or site: operators.
    
    Args:
        url: The full URL to extract content from (e.g., "https://example.com/page")
        
    Returns:
        The extracted content from the URL
    """
    try:
        result = tavily_client.extract(urls=[url])
        # Tavily retourne une liste de résultats
        if result and len(result) > 0:
            return result[0].get("content", "No content extracted")
        return "No content extracted"
    except Exception as e:
        return f"Error extracting content: {str(e)}"

tools = [TavilySearch(), extract_url_content]
llm = ChatOpenAI(model="gpt-4")
react_prompt = hub.pull("hwchase17/react")
output_parser = PydanticOutputParser(pydantic_object=AgentResponse)
react_prompt_with_format_instructions = PromptTemplate(
    template=REACT_PROMPT_WITH_REACT_INSTRUCTIONS,
    input_variables=["input", "agent_scratchpad", "tool_names"]
).partial(format_instructions=output_parser.get_format_instructions())

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt_with_format_instructions,
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

def extract_and_parse(x):
    """Extract output and parse it, with error handling"""
    try:
        output = x["output"]
        parsed = output_parser.parse(output)
        return parsed
    except Exception as e:
        # Si le parsing échoue, retourner au moins l'output brut
        print(f"⚠️ Parsing error: {e}")
        print(f"Raw output: {x.get('output', 'No output')}")
        return {"answer": x.get("output", "No answer"), "sources": []}

chain = agent_executor | RunnableLambda(extract_and_parse)


def main():
    result = chain.invoke(
        input={
            "input": "Trouve moi 3 offres d'emploi à Paris sur Linkedin pour un ingénieur IA avec Langchain dans le poste",
        }
    )
    print("\n" + "="*50)
    print("RÉSULTAT FINAL:")
    print("="*50)
    # result est un objet AgentResponse (Pydantic), pas un dict
    if isinstance(result, AgentResponse):
        print(f"Answer: {result.answer}")
        print(f"\nSources ({len(result.sources)}):")
        for i, source in enumerate(result.sources, 1):
            print(f"  {i}. {source.url}")
    else:
        # Fallback si c'est un dict
        print(f"Answer: {result.get('answer', 'N/A')}")
        print(f"\nSources ({len(result.get('sources', []))}):")
        for i, source in enumerate(result.get("sources", []), 1):
            print(f"  {i}. {source.url if isinstance(source, Source) else source.get('url', 'N/A')}")
    print("="*50)


if __name__ == "__main__":
    main()
