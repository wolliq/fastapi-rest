import requests

# URL of the scoring endpoint
url = "http://localhost:8000/score"

# Vector to be scored
vector = [0.1, 0.2, 0.3, 0.4]

# Create the payload
payload = {"data": [vector]}

# Send the POST request
response = requests.post(url, json=payload)

# Check the response
if response.status_code == 200:
    result = response.json()
    predictions = result["predictions"]
    print("Predictions:", predictions)
else:
    print("Error:", response.status_code)