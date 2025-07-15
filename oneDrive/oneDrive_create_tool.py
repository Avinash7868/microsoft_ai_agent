from langchain.tools import Tool
import requests
import os
import json

ACCESS_TOKEN = requests.get('http://localhost:3002/microsoft/access-token').text
HEADERS = {"Authorization": f"Bearer EwBoBMl6BAAUBKgm8k1UswUNwklmy2v7U/S+1fEAAcGYDnc0c1f/HJX6sg5mqIPFW0TFpePXw16xjaNpyDGN/PQYnwU4L2pPZKRC5tkY65RyTHc8VzCN5+sfVGbgL/BV8eZuLnS3B5fin0Qo2F0MdHon6OVVdBtB6n/5fFC3XhBv1WrKlhlaRVq82xe6dYLzBQzgeGWeZBW5WAz3HSYOodLz7PcVbtrWDeaQMny2Z5Jh7EzqhPp83ySMHDVVRlG7Fo2FK1fF00W7SFsFs14Yqag+Ynut/HrWczkgy7A3lZ9slBsebXcT+nYNe5BAhpwcpx/V6UlaDdn0Yn9F16k+ewVJ+uFHGXsQ1ipzLNZbAGqIwg6t7noA6wdquz0hyTsQZgAAEAXoLSdkJyxMKVXWpDaHQRswA6O4iHSnVzEzoaVJX6VUNcwaf+WVWuuLROZDWEEEapwMjhlxss2mqedvTDl8S9kCeiGQt6LxuZljk6yC/sAYPlukwKw3aZ9Fz3JE63M+wF/BIDstIHsgp+JmsU54MW+8m7BYT9WYnZ5MpIzKpRa/nFkTjyMz5XH5rCzHmlhGEixSYmRJYRLLKidSQygoPjHtCvjktCEkXsbmVBI+P/hlFxbXfSLhE69i8ahwWtKp8vZFVXF2HqQPMaCRz0XcbqXhNQR79F+vgS5JzZrZdB6fB/AOPTgdjIWf6nW0SfpjoB7nqOtRgSXATU/ZkssnhxYsZj8W5Mm294LwO8b0U8YckL3FgOxGo2V4BCPSHpXAgeuQJSWBVTnZVF9TDay1gFTMw7h3HPWZ0fJCX901ZUrmm+9573L9ZmTjmtsbMoOlrvI7QwVtKKHfXGFt5/8o43RZwW0NVVJYFQc64GGKLN+5e5B4TBr5XeRM0YnVwuRODCjGF+aA34jHivFI8eNTPF4gSz3UxCos9/JB00HKN67w0sJZW2YhGVrbKpnUneuzLcU4uVsBQKE8wAZIjh6wekuKIwqeTEgQxn6zuKAaTnY9zcZ6UswdvukUHGtmXH6cMHRS9849FsMMN/2j99JpXA+2B9u58N2VG4x2teRm3NoJEH9xqScXCcXngsL2az5dQlZ2H9nAqVAURMUL+mT/+CHmRorhkgJohKXuZ30HZ15Rhu6XPWsOQ5PWZzJtBn0Jc5nSwsOoJgh2L//x3T9yrzJIVsAEi1SejU17Y9W7+R9Ewal/p1ho0wqPuPAOTtZGWvqrXclq6L6ipdvnsK60dNA9dK+PHOx4Yh9bVTos8YbSSlzesfukgPpGpZlB6bnluTmfNsjob1o2rOoClwS4pii9K9BrunFQVGCN6aRak5M5yUY+tCd6lQuOt3vw9qO98rYAWIRbL1GEaMu1XfXfxiog3+EdtIA74U3iPZ27Qi81SiWzHsCwp3T6C6B3S6weGMnGtrXcMFMNX9Qp94sz9giTL5hCHdoRqj0jpdfk1eKsS0TRJejF4BmEK4NYgMpXjyHjcSx5jJKezg5M4Zazg/ur0WMD"}
API_BASE_URL = "https://graph.microsoft.com/v1.0"

def create_folder(parent_id: str, folder_name: str):
    url = f"{API_BASE_URL}/drive/items/{parent_id}/children"
    payload = {
        "name": folder_name,
        "folder": {},
        "@microsoft.graph.conflictBehavior": "rename"
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json() if response.status_code in (200, 201) else f"Failed: {response.text}"

def delete_item(item_id: str):
    url = f"{API_BASE_URL}/drive/items/{item_id}"
    response = requests.delete(url, headers=HEADERS)
    return "Deleted successfully." if response.status_code == 204 else f"Failed: {response.text}"

def upload_file(parent_id: str, filename: str, file_content: bytes):
    url = f"{API_BASE_URL}/drive/items/{parent_id}:/{filename}:/content"
    headers = HEADERS.copy()
    headers["Content-Type"] = "application/octet-stream"
    response = requests.put(url, headers=headers, data=file_content)
    return response.json() if response.status_code in (200, 201) else f"Failed: {response.text}"

def copy_item(item_id: str, parent_reference_json: str, name: str = None):
    url = f"{API_BASE_URL}/drive/items/{item_id}/copy"
    body = {"parentReference": eval(parent_reference_json)}
    if name:
        body["name"] = name
    response = requests.post(url, headers=HEADERS, json=body)
    return response.json() if response.status_code in (200, 202) else f"Failed: {response.text}"

def move_item(item_id: str, parent_reference_json: str):
    url = f"{API_BASE_URL}/drive/items/{item_id}"
    body = {"parentReference": json.loads(parent_reference_json)}
    response = requests.patch(url, headers=HEADERS, json=body)
    return response.json() if response.status_code in (200, 201) else f"Failed: {response.text}"

def create_sharing_link(item_id: str, link_type: str = "view"):
    url = f"{API_BASE_URL}/drive/items/{item_id}/createLink"
    body = {"type": link_type}
    response = requests.post(url, headers=HEADERS, json=body)
    return response.json() if response.status_code in (200, 201) else f"Failed: {response.text}"

def invite_users(item_id: str, recipients_json: str, message: str):
    url = f"{API_BASE_URL}/drive/items/{item_id}/invite"
    body = {
        "recipients": json.loads(recipients_json),
        "message": message
    }
    response = requests.post(url, headers=HEADERS, json=body)
    return response.json() if response.status_code in (200, 201) else f"Failed: {response.text}"

def remove_permission(item_id: str, perm_id: str):
    url = f"{API_BASE_URL}/drive/items/{item_id}/permissions/{perm_id}"
    response = requests.delete(url, headers=HEADERS)
    return "Permission removed successfully." if response.status_code == 204 else f"Failed: {response.text}"

onedrive_create_tools = [
    Tool(
        name="CreateFolder",
        func=lambda args: create_folder(*args.split("|")),
        description="Create a folder in OneDrive. Input should be 'parent_id|folder_name'."
    ),
    Tool(
        name="DeleteItem",
        func=lambda item_id: delete_item(item_id),
        description="Delete an item from OneDrive. Input should be the item ID."
    ),
    Tool(
        name="UploadFile",
        func=lambda args: upload_file(*args.split("|")),
        description="Upload a file to OneDrive. Input should be 'parent_id|filename|file_content'."
    ),
    Tool(
        name="CopyItem",
        func=lambda args: copy_item(*args.split("|")),
        description="Copy an item in OneDrive. Input should be 'item_id|parent_reference_json|name'."
    ),
    Tool(
        name="MoveItem",
        func=lambda args: move_item(*args.split("|")),
        description="Move an item in OneDrive. Input should be 'item_id|parent_reference_json'."
    ),
    Tool(
        name="CreateSharingLink",
        func=lambda args: create_sharing_link(*args.split("|")),
        description="Create a sharing link for a OneDrive item. Input should be 'item_id|type'. Type is usually 'view', 'edit', or 'embed'."
    ),
    Tool(
        name="InviteUsers",
        func=lambda args: invite_users(*args.split("|")),
        description="Invite users to a OneDrive item. Input should be 'item_id|recipients_json|message'. 'recipients_json' should be a JSON list of recipient objects."
    ),
    Tool(
        name="RemovePermission",
        func=lambda args: remove_permission(*args.split("|")),
        description="Remove a permission from a OneDrive item. Input should be 'item_id|perm_id'."
    ),
    # Add more create/upload tools as needed
]