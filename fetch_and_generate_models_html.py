import requests
import markdown2

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

url = "https://cryptotalks.ai/v1/get_models/"
models = get_models(url)
html_content = generate_html(models)

file_path = "models_list.html"
with open(file_path, "w") as file:
    file.write(html_content)

print(f"HTML file created at {file_path}")
