from flask import Flask, request, jsonify
from flask_cors import CORS  # Add this import
from langchain.agents import initialize_agent, AgentType
# from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from oneNote.oneNote_create_tools import onenote_create_tools
from oneNote.oneNote_get_tools import onenote_get_tools
from ToDo.todo_get_tools import todo_get_tools
import dotenv
import os

# Load .env
dotenv.load_dotenv()

# Ensure access token
if not os.getenv("GRAPH_ACCESS_TOKEN"):
    raise ValueError("GRAPH_ACCESS_TOKEN not found in .env")


if not os.getenv("AZURE_OPENAI_API_KEY") or not os.getenv('AZURE_OPENAI_API_INSTANCE_NAME') or not os.getenv("AZURE_OPENAI_API_DEPLOYMENT_NAME"):
    raise ValueError("Azure OpenAI credentials not found in environment variables.")

# Flask setup
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# Initialize LLM & tools
llm = AzureChatOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=f"https://{os.getenv('AZURE_OPENAI_API_INSTANCE_NAME')}.openai.azure.com/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_API_DEPLOYMENT_NAME"),
    # model="gpt-35-turbo",
    # temperature=0,
    # max_retries=2,
    # max_tokens can be set if needed, e.g. max_tokens=2048
)
tools = onenote_create_tools + onenote_get_tools + todo_get_tools # both are lists

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

@app.route("/run-agent", methods=["POST"])
def run_agent():
    data = request.get_json()
    print(data, "-------------data")
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' in request"}), 400
    try:
        verify = data['agent']
        if verify == "Avi":
            response = agent.invoke(data["prompt"])
            return jsonify({"response": response})
        else:
            return "Unauthorized"
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
