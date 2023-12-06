import requests
import json

# Replace the URL with your actual API endpoint
api_url = 'http://127.0.0.1:8000/cs411project_app/get_roadtrip/'

# Replace the payload with your actual request data
payload = {
    'origin': 'New York, NY',
    'destination': 'Miami, FL',
    'is_direct_route': False,
    'distance_limit': 500,
    'start_date': '2023-12-15',
}

headers = {'Content-Type': 'application/json'}

# Make a POST request
response = requests.post(api_url, data=json.dumps(payload), headers=headers)

# # Print the response
# print(response.status_code)
# print(response.json())  # Assuming the response is in JSON format

json.dump(response.json(), open('sample_api_output.json', 'w'), indent=4)