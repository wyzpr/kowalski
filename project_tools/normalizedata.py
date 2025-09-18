from dotenv import load_dotenv
import json, time, random
from openai import RateLimitError
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

load_dotenv()


import json


#we get a dict that can now be modified. The question is, can llms give me the prompts I need?

class CVAnalysis(BaseModel):
    labels: list[str]

llm = ChatOpenAI(model_name="gpt-4")
parser = PydanticOutputParser(pydantic_object=CVAnalysis)

prompt = ChatPromptTemplate.from_messages([
    (
    "system", 
    """You are a CV labeling agent. You will be provided with the text of a user's CV. Your task is to figure out the 
    job category or industry the CV is targeting (e.g., Software Engineer, Data Scientist, Marketing Manager) and label them using single words only (Software, Data, Marketing in these cases). 
    Take superfluous words like manager, engineer etc. aside and add them as a separate label. These will be used to tag and categorize the CV.
    Create a list of all possible jobs or key words the CV may be targeting.
    For example, someone with a computer science degree could be pursuing roles in software engineering, data science, game development, IT consulting and much more.
    I want a list of key words that I can use to label the CV. Use only basic job terms like "Software", "Data", "Marketing", "IT", "Product", "Sales" etc.
    If you are unsure, make the best guess. If the CV is very generic, use "General".
    If specific skills or technologies are mentioned, include relevant job titles associated with those skills or the name of the technology itself.
    Provide output as a list of strings and use no other text.\n{format_instructions}"""
    ),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
]).partial(format_instructions=parser.get_format_instructions())

tools = []

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

#verbose=True to see the agent's thought proces

agent_executor = AgentExecutor(agent=agent, tools = tools, handle_parsing_errors=True)

target_file = open("./data/resumes/LabelDataset.json", mode="a", encoding="utf-8")

with open("./data/resumes/BasicDataset.json", mode="r", encoding="utf-8") as read_file:
    data = read_file.readlines()
    i = 0
    size = len(data)

    while i < size:
        print(f"Processing resume {i+1} of {size}")
        line = data[i]
        failedAttempt = 0
        formatted = {}
        resume = json.loads(line)
        formatted['Category'] = resume['Category']
        formatted['Resume'] = resume['Resume']

        try:
            raw_response = agent_executor.invoke({"query": resume['Resume'], "name": "LabelAgent"})   
            structured_response = parser.parse(raw_response['output'])
            formatted['Labels'] = structured_response.labels
            json.dump(formatted, target_file, ensure_ascii=True)
            target_file.write("\n")
            i += 1
        except RateLimitError as e:
            failedAttempt += 1
            wait = (2 ** failedAttempt) + random.random()
            print(f"Rate limited. Waiting {wait:.2f}s...")
            time.sleep(wait)
        except Exception as e:
            print("Failed to parse response:", e)
            print("Raw response:", raw_response['output'])


    target_file.close()

##22.57, after 122 we have 20.53