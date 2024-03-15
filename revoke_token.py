import requests
import json

def revoke_token(url, auth_token, token_to_revoke):
    headers = {
        'Authorization': f'bearer {auth_token}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "token": token_to_revoke
    })
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to revoke token. Status code: {response.status_code}, Response: {response.text}")
        return {}

url = "https://cryptotalks.ai/v1/revoke_token/"
auth_token = "your_api_token_here"  # The token used for authentication
token_to_revoke = "your_api_token_here"  # The token you want to revoke

revoke_response = revoke_token(url, auth_token, token_to_revoke)

if revoke_response:
    print("Revoke Response:", revoke_response)
else:
    print("Could not revoke token.")
