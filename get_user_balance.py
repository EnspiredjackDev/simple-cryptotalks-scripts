import requests

def get_user_balance(url, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("Unauthorized. Check if the token is correct and has the required permissions.")
        return {}
    else:
        print(f"Failed to get user balance. Status code: {response.status_code}, Response: {response.text}")
        return {}

url = "https://cryptotalks.ai/v1/get_user_balance/"
token = "your_api_token_here"  # Replace 'your_api_token_here' with your actual API token

balance_info = get_user_balance(url, token)

if balance_info:
    print("User Balance:", balance_info['balance'], "USD")
else:
    print("Could not retrieve user balance.")
