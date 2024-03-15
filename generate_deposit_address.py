import requests
import json

def generate_deposit_address(url, token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'bearer {token}'  
    }
    payload = json.dumps({"token": token})
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 201:
        return response.json()
    elif response.status_code == 401:
        print("Unauthorized. Check if the token is correct and has the required permissions.")
        return {}
    else:
        print(f"Failed to generate deposit address. Status code: {response.status_code}, Response: {response.text}")
        return {}

url = "https://cryptotalks.ai/v1/generate_deposit_address/"
token = "your_api_token_here"  # Replace 'your_api_token_here' with your actual API token

deposit_address = generate_deposit_address(url, token)

if deposit_address:
    print("Deposit Address:", deposit_address['addresses'])
else:
    print("No deposit address generated.")
