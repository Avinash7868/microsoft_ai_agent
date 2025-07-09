from flask import Flask, request, jsonify
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from oneNote.oneNote_create_tools import onenote_create_tools
from oneNote.oneNote_get_tools import onenote_get_tools
import dotenv
import os

# Load .env
dotenv.load_dotenv()

# Ensure access token
if not os.getenv("GRAPH_ACCESS_TOKEN"):
    raise ValueError("GRAPH_ACCESS_TOKEN not found in .env")

# Flask setup
app = Flask(__name__)

# Initialize LLM & tools
llm = ChatOpenAI(temperature=0)
tools = onenote_create_tools + onenote_get_tools  # both are lists

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

@app.route("/run-agent", methods=["POST"])
def run_agent():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' in request"}), 400
    try:
        response = agent.run(data["prompt"])
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
