from langchain.tools import Tool
import requests
import os
from bs4 import BeautifulSoup

# Load token from env or secret manager
ACCESS_TOKEN = requests.get('http://localhost:3000/microsoft/access-token').text
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
# Get Sections from a Specific Notebook
# -------------------------
def get_sections(notebook_id: str):
    url = f"https://graph.microsoft.com/v1.0/me/onenote/notebooks/{notebook_id}/sections"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        sections = response.json().get("value", [])
        return "\n".join([f"{sec['displayName']} (ID: {sec['id']})" for sec in sections])
    return f"Failed to fetch sections: {response.text}"

# -------------------------
# Get all Sections
# -------------------------
def get_all_sections():
    url = "https://graph.microsoft.com/v1.0/me/onenote/sections"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        sections = response.json().get("value", [])
        return "\n".join([f"{sec['displayName']} (ID: {sec['id']})" for sec in sections])
    return f"Failed to fetch sections: {response.text}"

# -------------------------
# Get Pages from a Specific Section
# -------------------------
def get_pages(section_id: str):
    url = f"https://graph.microsoft.com/v1.0/me/onenote/sections/{section_id}/pages"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        pages = response.json().get("value", [])
        return "\n".join([f"{page['title']} (ID: {page['id']})" for page in pages])
    return f"Failed to fetch pages: {response.text}"

# -------------------------
# Get all Pages
# -------------------------
def get_all_pages():
    url = "https://graph.microsoft.com/v1.0/me/onenote/pages"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        pages = response.json().get("value", [])
        return "\n".join([f"{page['title']} (ID: {page['id']})" for page in pages])
    return f"Failed to fetch pages: {response.text}"

# ------------------
# Get Pages Content
# ------------------
def get_page_content(page_id: str):
    url = f"https://graph.microsoft.com/v1.0/me/onenote/pages/{page_id}/content"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    return f"Failed to fetch page content: {response.text}"

onenote_get_tools = [
    Tool(
        name="GetNotebooks",
        func=lambda _: get_notebooks(),
        description="Retrieve all notebooks for the signed-in user."
    ),
    Tool(
        name="GetSections",
        func=lambda notebook_id: get_sections(notebook_id),
        description="Retrieve all sections in a specific notebook. Input should be the notebook ID."
    ),
    Tool(
        name="GetAllSections",
        func=lambda _: get_all_sections(),
        description="Retrieve all sections across all notebooks."
    ),
    Tool(
        name="GetPages",
        func=lambda section_id: get_pages(section_id),
        description="Retrieve all pages in a specific section. Input should be the section ID."
    ),
    Tool(
        name="GetAllPages",
        func=lambda _: get_all_pages(),
        description="Retrieve all pages across all sections."
    ),
    Tool(
        name="GetPageContent",
        func=lambda page_id: get_page_content(page_id),
        description="Get content of a OneNote page. Input should be the page ID."
        # description="Get the exact raw HTML content of a OneNote page. Input should be the page ID. Return the HTML as-is, without summarizing or interpreting."
    )
]
