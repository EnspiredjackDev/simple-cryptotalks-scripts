
import requests
import json

def generate_token(url, email, password):
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({"email": email, "password": password})
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("Unauthorized. Check if the email and password are correct.")
        return {}
    else:
        print(f"Failed to generate token. Status code: {response.status_code}, Response: {response.text}")
        return {}

url = "https://cryptotalks.ai/v1/generate_token/"
email = "your_email_here"  # Replace 'your_email_here' with your actual email address
password = "your_password_here"  # Replace 'your_password_here' with your actual password

token_response = generate_token(url, email, password)

if token_response:
    print("Generated Token:", token_response['token'])
else:
    print("No token generated.")
