from langchain.tools import Tool
import requests
import os

def get_token():
    """
    Retrieve access token for Microsoft Graph API.
    This is used to authenticate requests.
    """
    response = requests.get('http://localhost:3000/microsoft/access-token')
    if response.status_code == 200:
        return response.text
    return f"Failed to fetch page content: {response.text}"

get_Token = [
    Tool(
        name="GetToken",
        func=lambda _: get_token(),
        description="Retrieve access token for Microsoft Graph API when access token expires. This is used to authenticate requests."
    ),
]