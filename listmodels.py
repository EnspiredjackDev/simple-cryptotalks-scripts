import requests

def get_models(url):
    response = requests.get(url)
    if response.status_code == 200:
        models = response.json()
        return models['data']
    else:
        print("Failed to fetch models. Status code:", response.status_code)
        return []

url = "https://cryptotalks.ai/v1/get_models/"
models = get_models(url)

for model in models:
    print(f"ID: {model['id']}, Name: {model['name']}, Description: {model['description'][:50]}...")
