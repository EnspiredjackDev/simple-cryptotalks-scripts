# simple-cryptotalks-scripts
These are some simple command line python scripts for use on [cryptotalks.ai](https://cryptotalks.ai/).  
Nothing fancy, just a script for every endpoint (except chat/completions) 

## webapp/
Webapplication front and backend for using the API to chat with models (unfinished)

#### webapp.py
Webapp backend, run with `python3 ./webapp.py` in the terminal.  

**Requirements:**  
`pip install flask flask_cors openai`

#### Angular frontend
Webapp frontend, not meant for production, not like any of the other things here really are.  
Run with `ng serve` in the terminal in the `./webapp/chat-frontend/` directory.  

**Requirements:**  
Node V18+  
Run `npm install` in the `./webapp/chat-frontend/` directory.

## walk_through.py
Step-by-step walkthrough cli tool of all the files in this repo - cli menu and all. (I think I got carried away with this one)  

**Requirements:**  
`pip install markdown2`  

All types of authentication in but not necessarily required.  

## listmodels.py
Gets and lists all the models available in the command line.

No authentication required.

## fetch_and_generate_models_html.py
Gets and lists all the models available in an html file that saves to the same directory the script is in.

**Requirements:**  
`pip install markdown2`  

No authentication required.

## create_user.py
Creates an account using an email and password.

**Authentication required:**  
`email`  
`password`  
`confirm_password`  
Replace `your_email_here`, `your_password_here` in the file with your correct credentials.  

## generate_token.py
Generates a new token using your username and password.  

**Authentication required:**  
`email`  
`password`  
Replace `your_email_here`, `your_password_here` in the file with your correct credentials.  

## generate_deposit_address.py
Generates a BTC and XMR deposit address with your API token.

**Authentication required:**  
`API_token`  
Replace `your_api_token_here` with your actual API token in the file.

## get_user_balance.py
Gets the balance of your account in USD.

**Authentication required:**  
`API_token`  
Replace `your_api_token_here` with your actual API token in the file.

## revoke_token.py
Revokes a token from your account.

**Authentication required:**  
`API_token`  
Replace `your_api_token_here` with your actual API token in the file.

**Other parameter:**  
`token_to_revoke`  
Replace ^ with your token to get revoked. (Make sure not to get them mixed up)
