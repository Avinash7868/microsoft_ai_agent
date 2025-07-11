from langchain.tools import Tool
import requests
import os
from bs4 import BeautifulSoup

# Load token from env or secret manager
ACCESS_TOKEN = os.getenv("GRAPH_ACCESS_TOKEN")
HEADERS = {
    "Authorization": f"Bearer EwBoBMl6BAAUBKgm8k1UswUNwklmy2v7U/S+1fEAAWOKolmIK92N4Mgdxn12sx4bthWenCTxERiZ21Zon6jrkmwT/hxmIdkg7577vNGoZyWcXPSSbu9y6JOg7cqgpi4QKj76cQKOQRG3ywrKG+cvQiuuBNiOqXTasEnSHp7PWy6ucvWbvEUCM6b8ZtsmROZepBUczRbphwMEprUKYVPSWt1ZBxiIB+KTDOQBnXTnf/tluh+EFETHfHp6IgX7JxkurVtIrQLuPqJ11Xzk+jHAcLqRcQDvHeZhNLOqxarhez4JvYTjWLEzlkZ/DN1G1DUj4vEgWFlEpgYD6f9e9WBMp5rY4w8Nw6Nj4NPAzeOkEWrEVhORdWskAiJnBWRk2BAQZgAAEOMTg5hu9nGOq34LpegEvR8wA3GBVx+mdFTSvZ9bUURc71hoEnMTM4IHj4A2ZOgisjjM0KvAym3M/gbz9uGXKBF/UCU030n6f2KGsnZNWLGLdNQxxFP3XAL/klVGTiws20rnahufr/yP96Oqc3LMTDhds0G76ogtZZM5RvKb5yrjxu84rU026kzfglrnqb8aTg+QkpEqWLKL5SJClMmar5RoH/0bKpi6DbmIkE0KkweSZtVRdlH6q+qDFFu8f7rNb29LI+j82TBa2/BLt/JaAbhJJOFg/nD1jedAicqhaRyJciQaLS8433TdOWF/NDAPVtrpgejtD6QD86RkAc3GZe7bkl1VgMFQJ85zJEcMQBFA9cUvq4+FbkMm/SCVwml8v5wAknNmC2s5njLLq6Ky7gKEhE/lmVQCMEbWoCfMh1TZJELGqi3eQwPN/exH5wdijGdiWztrWFVBR/efzgnmorhnHPOQMOi8yL62kl8dIqHy9t7C44ME8UoeYr+Q7phVFqHiP42J1+weYZRsKFJatj3wBCaszx1CBlmrjaIJvLGDEIEy6cDHH6wVl7PO0DRe4LbRfDQllXX8GzWOoQhtZq28QOERm9hYKdEdjGqkBn4YHwBoxTqsD4FBD7j5pa2tPA7zclFjiQtwvux8MBf8nFvu1f5DlH0TjYxS72pRngxYthiJmk+jJECIgmgC8mzZbh9ik6CCZHhPTjG7KjxUgxcOYpk8y0w/KirJM0LJSJH7P+KgGzmjF1H04Kli8/NHavRSbV4mc46FN8eZ91YJUA3wOkqoJfQJpwxY4DjIxz9+5nkB+/bzopYttwv04G12EnbZ0uz614JXlzWE63mVUz6oIOAy+g3iTMF01Ag+/YYP4L+tE9jmnHf0ujhmITQXg4We23dsNSoqXg2iqBHfQDyEqeQCsTme1A28MBWpmBm4ivaExXOyGS9uY6yrn4jjvfAJ3Twod67DO/MX0H4WfQTHA6FU+RAH30lt65xOuH3QhRO/zSteQE28vAQyEkGtgheqsr9asp8wJ03wlwAGf0P/CuurSbc/vTxnyEb9hmuLnrh3BK7B7WSP8J9pB2TyDMxHWH+FNieGXS6his6NQyEGWGMD",
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
