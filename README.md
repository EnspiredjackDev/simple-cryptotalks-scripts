# simple-cryptotalks-scripts
These are some simple command line python scripts for use on [cryptotalks.ai](https://cryptotalks.ai/).  
Nothing fancy, just a script for every endpoint (except chat/completions) 

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
