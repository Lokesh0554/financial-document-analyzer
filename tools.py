import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import tool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader

# Search tool
search_tool = SerperDevTool()

# CrewAI tool wrapper
@tool("Read Financial Document")
def read_data_tool(file_path: str = "data/sample.pdf") -> str:
    """Read and extract text from financial PDF"""

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    full_report = ""
    for page in docs:
        content = page.page_content
        while "\n\n" in content:
            content = content.replace("\n\n", "\n")
        full_report += content + "\n"

    return full_report
