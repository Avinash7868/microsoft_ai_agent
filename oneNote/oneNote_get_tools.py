from langchain.tools import Tool
import requests
import os

# Load token from env or secret manager
ACCESS_TOKEN = os.getenv("GRAPH_ACCESS_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# -------------------------
# Get Notebooks
# -------------------------
def get_notebooks():
    url = "https://graph.microsoft.com/v1.0/me/onenote/notebooks"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        notebooks = response.json().get("value", [])
        return "\n".join([f"{nb['displayName']} (ID: {nb['id']})" for nb in notebooks])
    return f"Failed to fetch notebooks: {response.text}"

# -------------------------
# Get Sections from a Notebook
# -------------------------
def get_sections(notebook_id: str):
    url = f"https://graph.microsoft.com/v1.0/me/onenote/notebooks/{notebook_id}/sections"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        sections = response.json().get("value", [])
        return "\n".join([f"{sec['displayName']} (ID: {sec['id']})" for sec in sections])
    return f"Failed to fetch sections: {response.text}"

# -------------------------
# Get Pages from a Section
# -------------------------
def get_pages(section_id: str):
    url = f"https://graph.microsoft.com/v1.0/me/onenote/sections/{section_id}/pages"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        pages = response.json().get("value", [])
        return "\n".join([f"{page['title']} (ID: {page['id']})" for page in pages])
    return f"Failed to fetch pages: {response.text}"

onenote_get_tools = [
    Tool(
        name="GetNotebooks",
        func=lambda _: get_notebooks(),
        description="Retrieve all notebooks for the signed-in user."
    ),
    Tool(
        name="GetSections",
        func=lambda notebook_id: get_sections(notebook_id),
        description="Get all sections from a notebook. Input should be the notebook ID."
    ),
    Tool(
        name="GetPages",
        func=lambda section_id: get_pages(section_id),
        description="Get all pages from a section. Input should be the section ID."
    )
]
