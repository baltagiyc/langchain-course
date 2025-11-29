REACT_PROMPT_WITH_REACT_INSTRUCTIONS = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

IMPORTANT INSTRUCTIONS:
- Use "tavily_search" for searching the web with search terms (e.g., "AI engineer Langchain Paris")
- Use "extract_url_content" when you have a specific URL and want to read its content
- NEVER use "tavily_search" with "Site:" operators or URLs alone - use "extract_url_content" for URLs
- When you find URLs in search results, use "extract_url_content" to read their content

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question: {format_instructions}

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""