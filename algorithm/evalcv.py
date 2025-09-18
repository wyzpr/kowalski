from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from readfile import read_file


load_dotenv()

class CVAnalysis(BaseModel):
    industry: str
    degree: str
    personal_summary: str
    skills: str
    experience: list[str]

llm = ChatOpenAI(model_name="gpt-4")
parser = PydanticOutputParser(pydantic_object=CVAnalysis)

prompt = ChatPromptTemplate.from_messages([
    (
    "system", 
    """You are a CV analysis agent. You will be provided with the file path to a user's CV. Use the read_file tool to extract the text from the CV.
Your task is to analyze the CV and extract all text in it that corresponds to sections in the following format:
1. Industry: Identify the job category or industry the CV is targeting (e.g., Software Engineer, Data Scientist, Marketing Manager). Mention only the category.
2. Degree: The highest degree or qualification obtained by the candidate (e.g., Bachelor of Science in Computer Science, Master of Business Administration). Mention only the degree.
3. Personal Summary: A brief summary of the candidate's professional background, skills, and career objectives.
4. Skills: A list of relevant skills, both technical and soft skills, that the candidate possesses. Keep only the important words and remove fluff.
5. Experience: A detailed list of previous job roles, including job titles, company names, durations, and key responsibilities or achievements. Keep only the important words and remove fluff.
If the CV contains multiple experiences, list each experience as a separate item in the experience list.
If any of these sections are missing in the CV, indicate "Not provided" for that section.
Provide the extracted information in a structured format as specified below. Ensure that the information is concise and relevant to the sections mentioned. 
    Wrap the output in this format and use no other text.\n{format_instructions}"""
    ),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
]).partial(format_instructions=parser.get_format_instructions())

tools = [read_file]

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

#verbose=True to see the agent's thought process
agent_executor = AgentExecutor(agent=agent, tools = tools, verbose=True, handle_parsing_errors=True)
query = input("Enter CV file path: ")
raw_response = agent_executor.invoke({"query": query, "name": "ResearchAgent"})

try:   
    structured_response = parser.parse(raw_response['output'])
    print("Category: ", structured_response.industry)
    print("Degree: ", structured_response.degree)
    print("Personal summary: ", structured_response.personal_summary)
    print("Skills: ", structured_response.skills)
    print("Experience: ", structured_response.experience)
except Exception as e:
    print("Failed to parse response:", e)
    print("Raw response:", raw_response['output'])



#/Users/jishnu/Documents/Work/Singha_Jishnu_CV_Draft1.docx