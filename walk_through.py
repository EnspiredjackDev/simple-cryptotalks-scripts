import requests
import json
import markdown2
import os

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

def generate_token(url, email, password):
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({"email": email, "password": password})
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        print("Token generated successfully.")
        return response.json()
    elif response.status_code == 401:
        print("Unauthorized. Check if the email and password are correct.")
        return {}
    else:
        print(f"Failed to generate token. Status code: {response.status_code}, Response: {response.text}")
        return {}

def generate_deposit_address(url, token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(url, headers=headers)
    
    if response.status_code == 201:
        print("Deposit address generated successfully.")
        return response.json()
    elif response.status_code == 401:
        print("Unauthorized. Check if the token is correct and has the required permissions.")
        return {}
    else:
        print(f"Failed to generate deposit address. Status code: {response.status_code}, Response: {response.text}")
        return {}
    
def get_models(url):
    response = requests.get(url)
    if response.status_code == 200:
        models = response.json()
        return models['data']
    else:
        print("Failed to fetch models. Status code:", response.status_code)
        return []

def generate_html(models):
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Models List</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; background-color: #f0f0f0; }}
        .model {{ background-color: #fff; border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; }}
        .model-header {{ color: #333; font-size: 20px; margin: 0 0 10px 0; }}
        .model-desc {{ color: #666; }}
    </style>
</head>
<body>
    <h1>Models List</h1>
    {models_html}
</body>
</html>
"""
    models_html = "".join([
        f"<div class='model'><div class='model-header'>{model['name']}</div><div class='model-desc'>{markdown2.markdown(model['description'])}</div></div>"
        for model in models
    ])
    return html_template.format(models_html=models_html)

def get_user_balance(url, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("User Balance retrieved successfully.")
        return response.json()
    elif response.status_code == 401:
        print("Unauthorized. Check if the token is correct and has the required permissions.")
        return {}
    else:
        print(f"Failed to get user balance. Status code: {response.status_code}, Response: {response.text}")
        return {}
    
def revoke_token(url, auth_token, token_to_revoke):
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({"token": token_to_revoke})
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        print("Token revoked successfully.")
        return response.json()
    else:
        print(f"Failed to revoke token. Status code: {response.status_code}, Response: {response.text}")
        return {}
    
def save_data_to_file(data, filename="user_data.json"):
    with open(filename, "w") as file:
        json.dump(data, file)

def load_data_from_file(filename="user_data.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return None

def get_user_consent():
    while True:
        print("\n\nDo you want to save your credentials for future use? (y/n)")
        print("Or just the Token? (t)")
        print("Warning: They will be stored as plaintext!")
        consent = input("(y/n/t): ").lower()
        if consent in ["y", "n", "t"]:
            return consent
        else:
            print("\nInvalid input. Please enter 'y', 'n', or 't'.\n")

def main_menu():
    consent = None
    user_data = load_data_from_file()
    email, password, token = '', '', ''

    if user_data is not None:
        load_from_stored = input("Load stored credentials? (y/n) ").lower()
        if load_from_stored == "y":
            email = user_data.get('email', '')
            password = user_data.get('password', '')
            token = user_data.get('token', '')
            print("Stored credentials loaded.")
        elif load_from_stored == "n":
            print("Proceeding without loading stored credentials.")

    while True:
        print("\nWelcome to CryptoTalks User Management")

        if not email or not password:
            print("1. Create a new user")
        print("2. Generate a token")
        print("3. Generate a deposit address")
        print("4. Get models")
        print("5. Fetch and Generate Models HTML")
        print("6. Get user balance")
        print("7. Revoke a token")
        print("8. Exit")

        choice = input("Please enter your choice: ")

        if choice == "1" and (not email or not password):
            url = "https://cryptotalks.ai/v1/create_user/"
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            confirm_password = input("Confirm your password: ")
            if password != confirm_password:
                print("Passwords do not match. Please try again.")
                continue
            user_creation_response = create_user(url, email, password, confirm_password)
            if user_creation_response:
                print("User Creation Response:", user_creation_response)
            else:
                print("User creation failed.")
            input("Enter - Continue")

        elif choice == "2":
            if not email:
                email = input("Enter your email: ")
            if not password:
                password = input("Enter your password: ")
            url = "https://cryptotalks.ai/v1/generate_token/"
            token_response = generate_token(url, email, password)
            if token_response:
                token = token_response.get('token', '')
                print("Generated Token:", token)
            else:
                print("No token generated.")
            input("Enter - Continue")

        elif choice == "3":
            if not token:
                token = input("Enter your token: ")
            url = "https://cryptotalks.ai/v1/generate_deposit_address/"
            deposit_address_response = generate_deposit_address(url, token)
            if deposit_address_response:
                print("Deposit Address:", deposit_address_response.get('addresses', 'No addresses found'))
            else:
                print("No deposit address generated.")
            input("Enter - Continue")
        
        elif choice == "4":
            url = "https://cryptotalks.ai/v1/get_models/"
            models = get_models(url)
            
            if models:
                print("\nAvailable Models:")
                for model in models:
                    print(f"ID: {model['id']}, Name: {model['name']}, Description: {model['description'][:50]}...")
            else:
                print("No models available.")
            input("Enter - Continue")
            
        elif choice == "5":
            url = "https://cryptotalks.ai/v1/get_models/"
            models = get_models(url)
            if models:
                html_content = generate_html(models)
                file_path = "models_list.html"
                with open(file_path, "w") as file:
                    file.write(html_content)
                print(f"HTML file created at {file_path}")
            else:
                print("Failed to fetch models or no models available.")
            input("Enter - Continue")

        elif choice == "6":
            url = "https://cryptotalks.ai/v1/get_user_balance/"
            if not token:
                token = input("Enter your token: ")
            balance_info = get_user_balance(url, token)
            if balance_info:
                print("User Balance:", balance_info['balance'], "USD")
            else:
                print("Could not retrieve user balance.")
            input("Enter - Continue")

        elif choice == "7":
            url = "https://cryptotalks.ai/v1/revoke_token/"
            if not token:
                token = input("Enter your token: ")
            token_to_revoke = input("Enter the token you wish to revoke: ")
            revoke_response = revoke_token(url, token, token_to_revoke)
            if revoke_response:
                print("Revoke Response:", revoke_response)
            else:
                print("Could not revoke token.")
            input("Enter - Continue")

        elif choice == "8":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
        
        if choice in ["1", "2", "3", "6", "7"] and (not user_data or load_from_stored == "n") and consent == None:
            consent = get_user_consent()
            if consent == "y":
                save_data_to_file({'email': email, 'password': password, 'token': token})
            elif consent == "t" and token:
                save_data_to_file({'token': token})

if __name__ == "__main__":
    main_menu()
