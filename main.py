from typing import List, Union
import os
from dotenv import load_dotenv
from langchain_classic.agents.output_parsers import ReActSingleInputOutputParser
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool, render_text_description, tool
from langchain_openai import ChatOpenAI

load_dotenv()

@tool
def get_text_length(text: str) -> int:
    """Get the length of a text"""
    print(f"get_text_length enter with {text}")
    # Enlève les guillemets simples, doubles et retours à la ligne au début/fin
    text = text.strip().strip("'\"").strip('\n')
    return len(text)


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    """Find a tool by its name"""
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found")

def main():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    print(f"OpenAI API Key: {openai_api_key}")
    print("Hello from langchain-course!")
    tools = [get_text_length]

    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!
    
    Question: {input}
    Thought:
    """

    tools_description = render_text_description(tools)
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=tools_description,
        tool_names=", ".join([t.name for t in tools]),
    )

    llm = ChatOpenAI(temperature=0, stop=["\nObservation", "Observation"])
    intermediate_steps = []
    agent = (
        {
            "input": lambda x: x["input"],
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser()
    )

    agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
        {
            "input": "What is the length of 'DOG' in characters?",
        }
    )
    print(agent_step)

    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        tool_to_use = find_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input

        observation = tool_to_use.func(str(tool_input))
        print(f"{observation=}")


if __name__ == "__main__":
    main()
