import requests
from ..locations import amadeus_key
# import amadeus_key
import json

AMADEUS_API_KEY = amadeus_key.amadeus_key
AMADEUS_API_SECRET = amadeus_key.amadeus_secret

AMADEUS_TOKEN_URL = 'https://test.api.amadeus.com/v1/security/oauth2/token'
AMADEUS_API_ENDPOINT = 'https://test.api.amadeus.com/'


# return an access token needed for Amadeus API calls
def get_amadeus_access_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=client_credentials&client_id={AMADEUS_API_KEY}&client_secret={AMADEUS_API_SECRET}"
    token = requests.post(AMADEUS_TOKEN_URL, headers=headers, data=data).json()
    return token['access_token']


# use the HotelList API to get basic hotel info around a lat-long within some radius
# token should be a token returned by get_amadeus_access_token
# radius is in miles
# returns a JSON
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


# use hotel search to get basic booking info given a list of hotel ids
# token should be a token returned by get_amadeus_access_token
# check_in_date and check_out_date are python datetime objects
# return a JSON
def search_hotel_from_id(token, hotel_ids, check_in_date, check_out_date):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    search_prefix = "v3/shopping/hotel-offers?"
    search_args = {
        "hotelIds": ','.join(hotel_ids),
        "adults": '1',
        "checkInDate": check_in_date.isoformat(),
        "checkOutDate": check_out_date.isoformat(),
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


# uses get_geocode_hotels and search_hotel_from_id to get basic booking info around a lat-long
# token should be a token returned by get_amadeus_access_token
# radius is in miles
# check_in_date and check_out_date are python datetime objects
# use only the first 10 hotel results
# return a JSON
def get_hotels_around_point(token, lat, long, radius, check_in_date, check_out_date):
    # make api calls
    geocoded = get_geocode_hotels(token, lat, long, radius)
    ids = [key['hotelId'] for key in geocoded][:10]
    searched = search_hotel_from_id(token, ids, check_in_date, check_out_date)

    # extract values
    # first geocode to get hotels around a point
    hotel_info = {}
    for hotel in geocoded:
        hotel_info[hotel['hotelId']] = {
            'name': hotel['name'],
            'distance': hotel['distance']['value']
        } | hotel['geoCode']

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
                'total': '$' + offer_details['price']['total'],
            }
        }

    valid_hotels = {hotel: hotel_info[hotel] for hotel in hotel_info if 'checkInDate' in hotel_info[hotel]}
    return valid_hotels

# test the functionality on lat-long of NYC
if __name__ == '__main__':
    access_token = get_amadeus_access_token()
    lat, long, radius = 40.7128, -74.0060, 1
    nyc_hotels = get_hotels_around_point(access_token, lat, long, radius)
    
    f = open('sample_hotel_list.txt', 'w')
    json.dump(nyc_hotels, f, indent=4)
