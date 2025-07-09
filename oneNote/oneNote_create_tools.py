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
# Create a new OneNote Notebook
# -------------------------
def create_notebook(name: str):
    url = "https://graph.microsoft.com/v1.0/me/onenote/notebooks"
    payload = {"displayName": name}
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        return f"Notebook '{name}' created successfully."
    return f"Failed to create notebook: {response.text}"

# -------------------------
# Create a new Section inside a Notebook
# -------------------------
def create_section(notebook_id: str, section_name: str):
    url = f"https://graph.microsoft.com/v1.0/me/onenote/notebooks/{notebook_id}/sections"
    payload = {"displayName": section_name}
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        return f"Section '{section_name}' created in notebook {notebook_id}."
    return f"Failed to create section: {response.text}"

# -------------------------
# Create a new Page inside a Section
# -------------------------
def create_page(section_id: str, title: str, body: str):
    url = f"https://graph.microsoft.com/v1.0/me/onenote/sections/{section_id}/pages"
    html_body = f"""
        <html>
            <head><title>{title}</title></head>
            <body>
                <p>{body}</p>
            </body>
        </html>
    """
    headers = HEADERS.copy()
    headers["Content-Type"] = "application/xhtml+xml"
    response = requests.post(url, headers=headers, data=html_body.encode("utf-8"))
    if response.status_code == 201:
        return f"Page '{title}' created in section {section_id}."
    return f"Failed to create page: {response.text}"

# -------------------------
# LangChain Tools
# -------------------------
onenote_create_tools = [
    Tool(
        name="CreateNotebook",
        func=lambda name: create_notebook(name),
        description="Create a new OneNote notebook. Input should be the notebook name."
    ),
    Tool(
        name="CreateSection",
        func=lambda args: create_section(*args.split("|")),
        description="Create a section in a notebook. Input should be 'notebook_id|section_name'."
    ),
    Tool(
        name="CreatePage",
        func=lambda args: create_page(*args.split("|")),
        description="Create a page in a section. Input should be 'section_id|page_title|page_body'."
    )
]
