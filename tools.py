from langchain_community.tools import WikipediaQueryRun
from ddgs import DDGS
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime


def save_to_txt(data: str, filename: str = "research_output.txt") -> str:
    """Saves content to a file and returns the file path."""
    formatted_text = f"--- Timestamp: {datetime.now().isoformat()} ---\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    return "Data saved to " + filename

save_tool = Tool(
    name="save_txt_to_file",
    func=save_to_txt,
    description="Saves the provided text data to a text file. Input should be the text to save."
)

search = DDGS()
search_tool = Tool(
    name="search",
    func=search.text,
    description="Search the web for recent information. Useful for when you need to find current events or verify facts. Input should be a search query."
)

wiki = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=wiki)