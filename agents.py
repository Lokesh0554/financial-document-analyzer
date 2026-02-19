import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import search_tool, read_data_tool

# LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.2,
    openai_api_key="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"
)
print("API KEY LOADED:", os.getenv("OPENAI_API_KEY")[:10])


# Financial Analyst
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents and extract insights based on the user query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a CFA-level financial analyst specializing in financial statement analysis, "
        "valuation and market research."
    ),
    tools=[read_data_tool, search_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=True
)

# Document Verifier
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify whether uploaded files are valid financial documents.",
    verbose=True,
    memory=True,
    backstory="You carefully inspect financial reports and verify document authenticity.",
    tools=[read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)

# Investment Advisor
investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide balanced investment insights based on financial data.",
    verbose=True,
    memory=True,
    backstory="You are a fiduciary investment advisor focused on long-term value.",
    tools=[search_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)

# Risk Analyst
risk_assessor = Agent(
    role="Financial Risk Analyst",
    goal="Evaluate financial and market risks.",
    verbose=True,
    memory=True,
    backstory="You specialize in market, liquidity and credit risk analysis.",
    tools=[read_data_tool, search_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)
