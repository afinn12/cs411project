import requests
import amadeus_api

AMADEUS_API_KEY = amadeus_api.amadeus_key
AMADEUS_API_SECRET = amadeus_api.amadeus_secret

AMADEUS_TOKEN_URL = 'https://test.api.amadeus.com/v1/security/oauth2/token'
AMADEUS_API_ENDPOINT = 'https://test.api.amadeus.com/'


def get_amadeus_access_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=client_credentials&client_id={AMADEUS_API_KEY}&client_secret={AMADEUS_API_SECRET}"
    token = requests.post(AMADEUS_TOKEN_URL, headers=headers, data=data).json()
    return token['access_token']


def args_to_str(prefix, args):
    return prefix + '&'.join([f"{key}={args[key]}" for key in args])


def get_geocode_hotels(token, lat, long, radius):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    geocode_prefix = "v1/reference-data/locations/hotels/by-geocode?"
    geocode_args = {
        "latitude": lat,
        "longitude": long,
        "radiusUnit": radius,
        "hotelSource": "ALL"
    }
    geocode_args_str = args_to_str(geocode_prefix, geocode_args)
    
    response = requests.get(AMADEUS_API_ENDPOINT + geocode_args_str, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        print(f"Error: {response.status_code} - {response.text}")
        raise Exception("Geocode Hotel ID Error")


def search_hotel_from_id(token, hotel_ids):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    search_prefix = "v3/shopping/hotel-offers?"
    search_args = {
        "hotelIds": ','.join(hotel_ids),
        "adults": '1',
        "checkInDate": "2023-12-15",
        "roomQuantity": '1',
        "paymentPolicy": "NONE",
        "includeClosed": "false",
        "bestRateOnly": "true"
    }
    search_args_str = args_to_str(search_prefix, search_args)

    response = requests.get(AMADEUS_API_ENDPOINT + search_args_str, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        print(f"Error: {response.status_code} - {response.text}")
        raise Exception("Search Hotel From ID Error")


if __name__ == '__main__':
    # make API calls
    access_token = get_amadeus_access_token()
    lat, long, radius = 40.7128, -74.0060, 5
    geocoded = get_geocode_hotels(access_token, lat, long, radius)
    geocoded.sort(key=lambda x: x['distance']['value'])
    ids = [key['hotelId'] for key in geocoded]
    searched = search_hotel_from_id(access_token, ids)
    
    # extract values
    
