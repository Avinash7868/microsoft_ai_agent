from langchain.tools import Tool
import requests
import os

# ACCESS_TOKEN = requests.get('http://localhost:3002/microsoft/access-token').text
HEADERS = {"Authorization": f"Bearer EwBoBMl6BAAUBKgm8k1UswUNwklmy2v7U/S+1fEAAdOnxixoTOY+cJLRlejCWvLQfTGPEz58ETAVVXlI+MOl6gbfYueHmNyIdMLH3YQUdz80xTtOG78YyfNqAs12k3BDuYeRP5tNn+HJR+pviPRb2JvOezicrxIervWR6MXnsqRREEiPwjKA6a+9RZeUr5J1IOIua9EAAnHFFhytJpc3Dvc9Gd6g2KPwDtwIecYzdM26G1Ze91oKDQlJbzFrNmwQRSQG4cGDOBsML68VdgCTh01zaF0bRhG1X6QLAVrfFMK8sodIjCTD8F1/eby+7ZixoDQIYiNEhRFWPYiu1iGl4jQCPEu/MHr+vTucqhp5I45pCxNFbkvredknvsPPGLkQZgAAEF1BTqYhQs3CH29dJwdr12gwA+Hzc8v05ih90ERfV13aOrS7PToQSNlv2Ek5j8IDoxtCB2O93Dctj4DGdNB4pz5yoJuJLGv4ZddpOBAPQkCz6vziA+ZXjLLXh7Ecqi8dYC/BRRBepcua5iYMAOjhhMYSJeMxAQVSDENPXXzi2Y8uwIb5GpoFQ8Fe0Bc49qbyTjBJ9UneaPsJSLK4W0fYRpxqnLSY5ibjTVbTXaK1cdBPa7sqM6TZX7QdGkEJ0F0MkFiLTm0YduebkZ8nJEk+F4v/rZhcDwXYx5AC7ivAcCTo5W9CE8NSngXSSKIKLdByMQi2m0kCLHQ5Sl2d4U/ix3y3MTImE6OT1JKD/goG6p/HnowXdQlpASpqntwes6WHoWKizqDVD7H1zwkCKqFNV8a23LC5N6DV3E34EYUeMeNiZRWOxUqsEpPNnZ5yO47lgJM5ZDet5X5f3aJx0NPr6RCoy4rTiSI6Mm6fQojBIkanh45A8gLOyZ7NYE6BY98QJx5qGJDJmyFBFEKISoRTk/tNDpBA1X7Cm7iG8KdKItvgi9Ngr1WX4yv4kFTOyUhk5dJpeLs92WOa5QkPPV9BX7VgSj3jQavkJC4hcUqoa9RBHj+jA7hrgxzMNJ0gOVGxi42KD24/Nfo4Voea9zgHqEmF1scd7H5cc1hc+3iQparK12Ai+JOgY8MqmwfIDcIzhjb3tQdwqnzmvLiQYrkdomczVGeyMJBAX9nzzpOfW4w9barIoLGuaCcF05JZLsN6GXm2ZaOiYymwOcGZ4tE5cBARW5CYyGhvtJVp0oDaCF4XuQe7uaj0vZKU3qX/V3AXNNCcxFkpgjmVvVao33fGf9TRLtNf6VbAOmMo9VA7zAeGzZaJwiQyVMXeItsw3YQsMKU++5jglz84CCCRlMh8qlOCbGUJu3XUFIJTSfXyKiAMzJ+g6GSnPi5pTLMY5aplKjo4Xr9J2y6/cg6IE7Aau9L8/zc7TxTR987dWl8tUPyMJNBzPbpw05dVuH/el4uiRbX5ARErhi4A7J9bd3bJdY3qVNGcIF7ETw45mSl+Ay1ajqlPs7S0FzAj98Ovfaf2JRysVbPw1zUiOCQtUFoixIySpmMD"}
API_BASE_URL = "https://graph.microsoft.com/v1.0"

def list_root_children():
    url = f"{API_BASE_URL}/me/drive/root/children"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else f"Failed: {response.text}"

def access_by_path(item_path: str):
    url = f"{API_BASE_URL}/drive/root:/{item_path}"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else f"Failed: {response.text}"

def list_children_of_item(item_id: str):
    url = f"{API_BASE_URL}/drive/items/{item_id}/children"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else f"Failed: {response.text}"

def search_drive(query: str):
    url = f"{API_BASE_URL}/drive/search(q='{query}')"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else f"Failed: {response.text}"

def download_file(item_id: str):
    url = f"{API_BASE_URL}/me/drive/items/{item_id}"
    response = requests.get(url, headers=HEADERS)
    return response.json()['@microsoft.graph.downloadUrl'] if response.status_code == 200 else f"Failed: {response.text}"



onedrive_get_tools = [
    Tool(
        name="ListRootChildren",
        func=lambda _: list_root_children(),
        description="List all items in the root of the user's OneDrive."
    ),
    Tool(
        name="AccessByName",
        func=lambda path: access_by_path(path),
        description="Access a OneDrive item by its name. Input should be the item name."
    ),
    Tool(
        name="ListChildrenOfItem",
        func=lambda item_id: list_children_of_item(item_id),
        description="List all children of a OneDrive item. Input should be the item ID."
    ),
    Tool(
        name="SearchDrive",
        func=lambda query: search_drive(query),
        description="Search OneDrive for items matching the query. Input should be the search query."
    ),
    Tool(
        name="DownloadFile",
        func=lambda item_id: download_file(item_id),
        description="Provides full link to download the file. Input should be the item ID."
    ),
]