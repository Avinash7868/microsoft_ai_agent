from langchain.tools import Tool
import requests
import os
import json

# ACCESS_TOKEN = requests.get('http://localhost:3002/microsoft/access-token').text
HEADERS = {"Authorization": f"Bearer EwC4BMl6BAAUBKgm8k1UswUNwklmy2v7U/S+1fEAAaYEkb79minYBjj/rG/5Wn/o4cBJ0z9+403uCJMtW++sLx9siNcLS+EBdulkI6TxwRGxdiC1IpJZn7LdluES+7gsBOjVujynuaUOLGd7QlMWKZxJ//rzJN7KIbH+taWngppXJm1hVa4iE7kHf08ZrCNKly15novQPwP1K6/7gPGiEp9LHy552xs7873/G/X81I7t8TM2jhM9f6eDr8KzZ35X51U/K5T2ZIw+CTrDlOwlvG+hpQQA0ZBvVBO00BGahx8mr67uwTV4kZ6nxmTps1hFw9T1VpBnCHBMY6Q6BPOvlJssJIY/LWSBwExhLP7C4CwyhxoAdL1K8AN6YJF16ooQZgAAEA54HPQYgwPSzKR+na5FbW6AAyqgqESulnx9ZILlqIuA9mIGenuSSEXditWpuML1W47rubC/TCf95LZzdSL/lLziYB15B9Hb8ofz/n6+UXdXmkwe/04GHddHlQqgg8m2bVsnrBwAiPPHLXZR5ShNz2ZPm7e+1lpgDspeBqqVdiQm3AS5vBaBZtMbH4q9KsAqfl4u9ktmrbZNqYV0u9G7jANT1BwL/ZhqKkVCou0AGZ/KReGB4CqpXJvpkuEUoJQftQVj8UlL1EaIY0w/g8ZlFeIhZ38GouOywP3PBdkYBmihNgYTPCIQUYMKtNLa61ab5/D4JnyQI3MUeV745iYtUH2ykGN8wPkk0jFUdilcjD1D8ApRl21yDK226hbaNo0s3xwrcv8gYJ8ZlOuTdDJM3SROvZIlaAljcn23J/NnS47+QWL3xETSnK7oT4mGluOhLImHUxt6BEBCds2Utinhm5ROjimprROoJ3RucRSETtaj+PFryb1yXv+3pjZZCI4izP3mGBa4xUO9RbYJYIj9f/Nzr0WuMb2VQmazFPpUa9ieqttw9dxc7AqTDBYNi4Q3M7GmwHGUoh8xs36s2GyF2XWhBGKxEWvrKvBZcghN5yoit73all2fzbOvTavxWus9TC39VcvHWOMcnSsyYsLqcUXH6IRW19WyERjyf3k5wpIazVntQ2/4ItYD4kYlv//mcXiYFyfLp4hBvpKKYoBMWqJT0PCZpAfm7SPBOa1SOVB6WOi0H2mArmO1TxZc9NPKf+55Q0CrRaUZH2a2fE5PG9+Z8/dyj9pruZwdhCD5G2uDtlbVuXPSXgmAdc7p+QdXX/LE3e9CMWoP33RlZCJLK2UuHIsU7gUbdGQ3bwZWQhnMtq9MTMhWI32gjnB7YsI8K2lusjQkM1zkC8i6XnYe592EiIgUBTe3GCNdz69mFPbQ61Tx1zYaLckDyO8fQP1MrG0aMVr+Ghg3+aheBN0sRQVzNGrt5SghNIuuy7L19Avw47TIQGUmxNfPrszgVQyzLfCBQK4de+Kg/SpwCtrvomuHT7NyTDv5osRH4nYvscrjfoGgnRY5W0fCO/bI3hJJjE/0U+M5gUf8O497JMcvlfdOUFInj2lIA7E1jLAFrcktKbVOZNLrKu4covb7Cd3/b2WO9AsMO4Q7Ks8r7uRfL2C7N7j29YcGuFuE1BgVWv2m0Q02U0j4+LefdznYIjH17egGzgM="}
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