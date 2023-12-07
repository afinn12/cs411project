import requests
import json

def roadtrip_test():
    api_url = 'http://127.0.0.1:8000/cs411project_app/get_roadtrip/'

    payload = {
        'origin': 'New York, NY',
        'destination': 'Miami, FL',
        'is_direct_route': False,
        'distance_limit': 500,
        'start_date': '2024-01-15',
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(api_url, data=json.dumps(payload), headers=headers)

    json.dump(response.json(), open('sample_api_output.json', 'w'), indent=4)

def sample_roadtrup_test():
    api_url = 'http://127.0.0.1:8000/cs411project_app/get_sample_roadtrip/'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, headers=headers)

    print(response.json())


if __name__ == '__main__':
    # sample_roadtrup_test()
    roadtrip_test()