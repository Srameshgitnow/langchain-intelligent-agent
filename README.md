🧠 LangChain Intelligent Agent (LLM + Calculator Routing)

This project demonstrates how to build an intelligent agent using LangChain and OpenAI GPT-4o-mini, capable of dynamically deciding whether to:

Perform arithmetic operations using a custom Calculator tool, or

Generate natural language reasoning using the LLM itself.

It uses LangChain’s RunnableBranch to route inputs based on intent — a simple but powerful concept for Agentic AI architectures.

====================================================================================================================================

📂 Repository Structure
.

├── dynamic_agent_with_langchain.ipynb       # (This code - hybrid routing demo)
├── README.md
├── .env.example                          # Template for API key storage
└── requirements.txt

====================================================================================================================================


🚀 Features

✅ Dynamic Tool Routing — The agent decides if an input is a math expression or a text query.
✅ Safe Evaluation — Uses a restricted eval environment for secure arithmetic.
✅ LangChain RunnableBranch — Elegant branching logic for modular reasoning.
✅ OpenAI GPT-4o-mini Integration — Handles non-math natural language queries.
✅ Extensible Design — Easily add more tools (e.g., weather, search, database).

====================================================================================================================================

💡 Example Usage
Input 1: Natural Language
print(agent_executor("What is the difference between AI Agents and Agentic AI?"))


🧩 Output (via LLM)

Agentic AI refers to systems capable of autonomous goal-directed behavior, 
while AI agents are the broader class of software entities that perceive and act. 
Agentic AI implies reasoning, planning, and adaptive decision-making.


Input 2: Arithmetic Expression
print(agent_executor("5373 + 138380 + 383838"))


🧮 Output (via Calculator)

527591

====================================================================================================================================

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/langchain-intelligent-agent.git
cd langchain-intelligent-agent

2️⃣ Create and Activate Virtual Environment
python -m venv venv
source venv/bin/activate       # (Linux/macOS)
venv\Scripts\activate          # (Windows)

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Environment Variable

Create a .env file in the root folder:

OPENAI_API_KEY=your_openai_api_key_here

====================================================================================================================================

🧩 Code Overview
🔹 Step 1: Define a Safe Calculator Tool
def safe_eval(expression: str) -> str:
    expression = re.sub(r"[^0-9+\-*/().]", "", expression)
    return str(eval(expression, {"__builtins__": {}}, {"add": operator.add, "sub": operator.sub}))

🔹 Step 2: Create a Tool
calculator_tool = Tool(
    name="Calculator",
    func=safe_eval,
    description="Performs basic arithmetic calculations (e.g., '5 + 10')."
)

🔹 Step 3: Branch Logic Using RunnableBranch
def decide_tool(input_text):
    return "calc" if re.search(r"\d+\s*[\+\-\*/]\s*\d+", input_text) else "llm"

branch = RunnableBranch(
    (lambda x: decide_tool(x) == "calc", math_chain),
    (lambda x: decide_tool(x) == "llm", text_chain),
    text_chain
)

🔹 Step 4: Execute Agent
def agent_executor(user_input):
    return branch.invoke(user_input)


====================================================================================================================================

🧠 Conceptual Architecture
 ┌──────────────────────┐
 │   User Input         │
 └─────────┬────────────┘
           │
     ┌─────▼─────┐
     │ decide_tool│
     └─────┬─────┘
     calc? │ llm?
 ┌─────────▼─────────┐      ┌────────────────┐
 │ Calculator Tool    │ or   │  ChatOpenAI LLM │
 └─────────┬─────────┘      └────────────────┘
           │
      ┌────▼────┐
      │ Response │
      └──────────┘


====================================================================================================================================

🔮 Future Enhancements

🧭 Add tool routing for APIs (e.g., weather, news)

🧠 Integrate memory & conversation context

🔄 Use LangGraph or AgentExecutor for multi-step reasoning

🧰 Extend schema extraction with custom structured outputs

====================================================================================================================================

📄 License

MIT License © 2025 [Your Name]