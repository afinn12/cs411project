import requests
import amadeus_api

AMADEUS_API_KEY = amadeus_api.amadeus_key
AMADEUS_API_SECRET = amadeus_api.amadeus_secret

AMADEUS_TOKEN_URL = 'https://test.api.amadeus.com/v1/security/oauth2/token'
AMADEUS_API_ENDPOINT = 'https://test.api.amadeus.com/v1/reference-data/locations/hotels/'


def get_amadeus_access_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=client_credentials&client_id={AMADEUS_API_KEY}&client_secret={AMADEUS_API_SECRET}"
    token = requests.post(AMADEUS_TOKEN_URL, headers=headers, data=data).json()
    return token['access_token']


def get_geocode_hotel_ids(lat, long, radius):
    access_token = get_amadeus_access_token()

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    geocode_args = {
        "latitude": lat,
        "longitude": long,
        "radiusUnit": radius,
        "hotelSource": "ALL"
    }
    geocode_args_str = "by-geocode?" + '&'.join([f"{key}={geocode_args[key]}" for key in geocode_args])
    
    response = requests.get(AMADEUS_API_ENDPOINT + geocode_args_str, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return [hotel['hotelId'] for hotel in data['data']]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        raise Exception("Geocode Hotel ID Error")

if __name__ == '__main__':
    lat, long, radius = 40.7128, -74.0060, 5
    print(get_geocode_hotel_ids(lat, long, radius))

