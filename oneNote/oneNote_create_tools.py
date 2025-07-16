from langchain.tools import Tool
import requests
import os
import time

# Load token from env or secret manager
try:
    ACCESS_TOKEN = requests.get('http://localhost:3000/microsoft/access-token').text
except:
    ACCESS_TOKEN = os.getenv("GRAPH_ACCESS_TOKEN")
HEADERS = {
    "Authorization": f"Bearer EwC4BMl6BAAUBKgm8k1UswUNwklmy2v7U/S+1fEAAaYEkb79minYBjj/rG/5Wn/o4cBJ0z9+403uCJMtW++sLx9siNcLS+EBdulkI6TxwRGxdiC1IpJZn7LdluES+7gsBOjVujynuaUOLGd7QlMWKZxJ//rzJN7KIbH+taWngppXJm1hVa4iE7kHf08ZrCNKly15novQPwP1K6/7gPGiEp9LHy552xs7873/G/X81I7t8TM2jhM9f6eDr8KzZ35X51U/K5T2ZIw+CTrDlOwlvG+hpQQA0ZBvVBO00BGahx8mr67uwTV4kZ6nxmTps1hFw9T1VpBnCHBMY6Q6BPOvlJssJIY/LWSBwExhLP7C4CwyhxoAdL1K8AN6YJF16ooQZgAAEA54HPQYgwPSzKR+na5FbW6AAyqgqESulnx9ZILlqIuA9mIGenuSSEXditWpuML1W47rubC/TCf95LZzdSL/lLziYB15B9Hb8ofz/n6+UXdXmkwe/04GHddHlQqgg8m2bVsnrBwAiPPHLXZR5ShNz2ZPm7e+1lpgDspeBqqVdiQm3AS5vBaBZtMbH4q9KsAqfl4u9ktmrbZNqYV0u9G7jANT1BwL/ZhqKkVCou0AGZ/KReGB4CqpXJvpkuEUoJQftQVj8UlL1EaIY0w/g8ZlFeIhZ38GouOywP3PBdkYBmihNgYTPCIQUYMKtNLa61ab5/D4JnyQI3MUeV745iYtUH2ykGN8wPkk0jFUdilcjD1D8ApRl21yDK226hbaNo0s3xwrcv8gYJ8ZlOuTdDJM3SROvZIlaAljcn23J/NnS47+QWL3xETSnK7oT4mGluOhLImHUxt6BEBCds2Utinhm5ROjimprROoJ3RucRSETtaj+PFryb1yXv+3pjZZCI4izP3mGBa4xUO9RbYJYIj9f/Nzr0WuMb2VQmazFPpUa9ieqttw9dxc7AqTDBYNi4Q3M7GmwHGUoh8xs36s2GyF2XWhBGKxEWvrKvBZcghN5yoit73all2fzbOvTavxWus9TC39VcvHWOMcnSsyYsLqcUXH6IRW19WyERjyf3k5wpIazVntQ2/4ItYD4kYlv//mcXiYFyfLp4hBvpKKYoBMWqJT0PCZpAfm7SPBOa1SOVB6WOi0H2mArmO1TxZc9NPKf+55Q0CrRaUZH2a2fE5PG9+Z8/dyj9pruZwdhCD5G2uDtlbVuXPSXgmAdc7p+QdXX/LE3e9CMWoP33RlZCJLK2UuHIsU7gUbdGQ3bwZWQhnMtq9MTMhWI32gjnB7YsI8K2lusjQkM1zkC8i6XnYe592EiIgUBTe3GCNdz69mFPbQ61Tx1zYaLckDyO8fQP1MrG0aMVr+Ghg3+aheBN0sRQVzNGrt5SghNIuuy7L19Avw47TIQGUmxNfPrszgVQyzLfCBQK4de+Kg/SpwCtrvomuHT7NyTDv5osRH4nYvscrjfoGgnRY5W0fCO/bI3hJJjE/0U+M5gUf8O497JMcvlfdOUFInj2lIA7E1jLAFrcktKbVOZNLrKu4covb7Cd3/b2WO9AsMO4Q7Ks8r7uRfL2C7N7j29YcGuFuE1BgVWv2m0Q02U0j4+LefdznYIjH17egGzgM=",
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
def create_section(notebook_id: str, section_name: str, retries=3, delay=2):
    url = f"https://graph.microsoft.com/v1.0/me/onenote/notebooks/{notebook_id}/sections"
    payload = {"displayName": section_name}
    for attempt in range(retries):
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code == 201:
            return f"Section '{section_name}' created in notebook {notebook_id}."
        # If transient error, retry
        try:
            error_json = response.json()
            if (
                response.status_code == 500 or
                error_json.get("error", {}).get("code") == "20280"
            ):
                if attempt < retries - 1:
                    time.sleep(delay)
                    continue
        except Exception:
            pass
        return f"Failed to create section: {response.text}"
    return f"Failed to create section after {retries} attempts: {response.text}"

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
        description="Create a page in a section. Input should be 'section_id|page_title|page_body'. If page_title or page_body is missing, generate them yourself. If the prompt includes 'summarize' or 'detail', create the content accordingly."
    )
]
