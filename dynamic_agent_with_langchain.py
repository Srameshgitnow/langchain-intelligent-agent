import operator
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import re
import getpass
import os
from dotenv import load_dotenv
load_dotenv()

# Define LLM
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")
# Initialize OpenAI LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, openai_api_key=os.environ["OPENAI_API_KEY"])

def safe_eval(expression: str) -> str:
    try:
        # Remove any non-math characters for safety
        expression = re.sub(r"[^0-9+\-*/().]", "", expression)
        return str(eval(expression, {"__builtins__": {}}, {"add": operator.add, "sub": operator.sub}))
    except Exception as e:
        return f"Error: {e}"

calculator_tool = Tool(
    name="Calculator",
    func=safe_eval,  # Uses the safe evaluation function
    description="Performs basic arithmetic calculations (e.g., '5 + 10')."
)

def decide_tool(input_text):
    return "calc" if re.search(r"\d+\s*[\+\-\*/]\s*\d+", input_text) else "llm"

math_chain = RunnableLambda(lambda x: x) | calculator_tool

text_chain = llm

branch = RunnableBranch(
    (lambda x: decide_tool(x) == "calc", math_chain),
    (lambda x: decide_tool(x) == "llm", text_chain),
    text_chain  # Default to LLM if no match
)

def agent_executor(user_input):
    return branch.invoke(user_input)

print(agent_executor("What is the difference between AI Agents and Agentic AI?"))  # Uses LLM
print(agent_executor("5373 + 138380 + 383838"))              # Uses Calculator