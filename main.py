from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from oneNote.oneNote_create_tools import onenote_create_tools
from oneNote.oneNote_get_tools import onenote_get_tools
import dotenv
import os

# Load environment variables from .env
dotenv.load_dotenv()

# Ensure access token is present
if not os.getenv("GRAPH_ACCESS_TOKEN"):
    raise ValueError("GRAPH_ACCESS_TOKEN not found in environment. Please set it in your .env file.")

# Initialize OpenAI LLM
llm = ChatOpenAI(temperature=0)

# tools
tools = [onenote_create_tools, onenote_get_tools]

# Initialize agent with tools
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Example runs
print("\nCreating notebook:")
print(agent.run("Create a OneNote notebook named 'LangChain Experiments'"))

print("\nCreating section:")
print(agent.run("Create a section called 'Ideas' in the notebook with ID 'YOUR_NOTEBOOK_ID'"))

print("\nCreating page:")
print(agent.run("Create a OneNote page titled 'Experiment 1' with body 'This is the first test.' in the section with ID 'YOUR_SECTION_ID'"))
