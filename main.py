from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools: list[str]

llm = ChatOpenAI(model_name="gpt-4")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages([
    (
    "system", 
    """You are a research assistant. Provide concise and accurate information.
    Answer the user's query based on the context provided and necessary tools.
    Wrap the output in this format and use no other text\n{format_instructions}"""
    ),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
]).partial(format_instructions=parser.get_format_instructions())

agent = create_tool_calling_agent(
    llm=llm,
    tools=[],
    prompt=prompt,
)

#verbose=True to see the agent's thought process
agent_executor = AgentExecutor(agent=agent, tools = [], verbose=True)

raw_response = agent_executor.invoke({"query": "Explain the theory of relativity and its implications in modern physics.", "name": "ResearchAgent"})

try:   
    structured_response = parser.parse(raw_response['output'])
    print(structured_response.topic)
    print(structured_response.summary)
    print(structured_response.sources)
except Exception as e:
    print("Failed to parse response:", e)
    print("Raw response:", raw_response['output'])