import requests


def get_nouns(text, url="http://127.0.0.1:8000/process-text/"):
    # The data you want to send in the POST request
    data = {
        'text': text
    }
    # Sending a POST request with the JSON payload
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the JSON response
        return response.json()
    else:
        return "Error:", response.status_code




