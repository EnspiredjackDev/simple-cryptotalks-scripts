import requests
import json

def create_user(url, email, password, confirm_password):
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({
        "email": email,
        "password": password,
        "confirm_password": confirm_password
    })
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 201:
        print("User created successfully.")
        return response.json()
    elif response.status_code == 400:
        print("Bad request. Possibly duplicate email or invalid data.")
        return {}
    else:
        print(f"Failed to create user. Status code: {response.status_code}, Response: {response.text}")
        return {}

url = "https://cryptotalks.ai/v1/create_user/"
email = "your_email_here"  # Replace with email
password = "your_password_here"  # Replace with password - Must be 8 characters or more
confirm_password = "your_password_here"  # Replace with password as confirmation

user_creation_response = create_user(url, email, password, confirm_password)

if user_creation_response:
    print("User Creation Response:", user_creation_response)
else:
    print("User creation failed.")
