import requests
import amadeus_key
import json

AMADEUS_API_KEY = amadeus_key.amadeus_key
AMADEUS_API_SECRET = amadeus_key.amadeus_secret

AMADEUS_TOKEN_URL = 'https://test.api.amadeus.com/v1/security/oauth2/token'
AMADEUS_API_ENDPOINT = 'https://test.api.amadeus.com/'


def get_amadeus_access_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=client_credentials&client_id={AMADEUS_API_KEY}&client_secret={AMADEUS_API_SECRET}"
    token = requests.post(AMADEUS_TOKEN_URL, headers=headers, data=data).json()
    return token['access_token']


def get_geocode_hotels(token, lat, long, radius):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    geocode_prefix = "v1/reference-data/locations/hotels/by-geocode?"
    geocode_args = {
        "latitude": lat,
        "longitude": long,
        "radius": radius,
        "radiusUnit": 'MILE',
        "hotelSource": "ALL"
    }
    
    response = requests.get(AMADEUS_API_ENDPOINT + geocode_prefix, headers=headers, params=geocode_args)

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
        "checkOutDate": "2023-12-16",
        "roomQuantity": '1',
        "currency": 'USD',
        "paymentPolicy": "NONE",
        "includeClosed": "false",
        "bestRateOnly": "true"
    }

    response = requests.get(AMADEUS_API_ENDPOINT + search_prefix, headers=headers, params=search_args)

    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        print(f"Error: {response.status_code} - {response.text}")
        raise Exception("Search Hotel From ID Error")


def get_hotels_around_point(token, lat, long, radius):
    # make api calls
    geocoded = get_geocode_hotels(token, lat, long, radius)
    # geocoded.sort(key=lambda x: x['distance']['value'])
    ids = [key['hotelId'] for key in geocoded]
    searched = search_hotel_from_id(token, ids)

    # extract values
    # first geocode to get hotels around a point
    hotel_info = {}
    for hotel in geocoded:
        hotel_info[hotel['hotelId']] = {
            'name': hotel['name'],
            'distance': hotel['distance']['value']
        } | hotel['geoCode']
    # print(hotel_info)
    # then use hotel ids to get offer details
    for offer in searched:
        offer_details = offer['offers'][0]
        hotel_info[offer['hotel']['hotelId']] |= {
            'checkInDate': offer_details['checkInDate'],
            'checkOutDate': offer_details['checkOutDate'],
            'roomInfo': offer_details['room']['typeEstimated'] | {
                'description': offer_details['room']['description']['text']
            },
            'guestInfo': offer_details['guests'],
            'price': {
                # 'base': '$' + offer_details['price']['base'],
                'total': '$' + offer_details['price']['total'],
            }
        }
    # print(hotel_info)
    valid_hotels = {hotel: hotel_info[hotel] for hotel in hotel_info if 'checkInDate' in hotel_info[hotel]}
    return valid_hotels

if __name__ == '__main__':
    access_token = get_amadeus_access_token()
    lat, long, radius = 40.7128, -74.0060, 1
    nyc_hotels = get_hotels_around_point(access_token, lat, long, radius)
    
    f = open('sample_hotel_list.txt', 'w')
    json.dump(nyc_hotels, f, indent=4)
