import requests
import yelp_key
import datetime
import json

YELP_API_KEY = yelp_key.yelp_key
YELP_API_ENDPOINT = 'https://api.yelp.com/v3/events'


# convert YYYY-MM-DD to unix time (total seconds since epoch)
def ymd_to_unix(date: str):
    date = datetime.datetime.fromisoformat(date)
    return int((date-datetime.datetime(1970,1,1)).total_seconds())


# use the Event Search API to get events around a lat-long within a radius
# radius is in miles
# TODO: add start and end dates as params
# returns a JSON
def search_event_from_latlong(lat, long, radius):
    headers = {
        'Authorization': f'Bearer {YELP_API_KEY}',
    }
    event_args = {
        'latitude': lat,
        'longitude': long,
        'limit': '15',
        'start_date': ymd_to_unix('2023-11-15'),
        'end_date': ymd_to_unix('2024-01-15'),
        'radius': radius*1609 # roughly the conversion from mile to meter
    }

    response = requests.get(YELP_API_ENDPOINT, headers=headers, params=event_args)

    if response.status_code == 200:
        data = response.json()
        return data['events']
    else:
        print(f"Error: {response.status_code} - {response.text}")
        raise Exception("Search Event From Lat Long Error")


# use search_event_from_lat_long to reformat the JSON for our needs
# radius is in miles
# TODO: add start and end dates as params
# return a JSON
def get_events_around_point(lat, long, radius):
    # make api call
    events = search_event_from_latlong(lat, long, radius)

    # extract relevant info
    event_info = {}
    fields = [
        'name', 'description', 'category', 'cost', 'event_site_url', 'latitude', 'longitude',
        'time_start', 'time_end'
    ]
    for event in events:
        event_info[event['id']] = {key:event[key] for key in fields}
    
    return event_info


# test the functionality on lat-long of NYC
if __name__ == '__main__':
    lat, long, radius = 40.7128, -74.0060, 1
    nyc_events = get_events_around_point(lat, long, radius)
    
    f = open('sample_event_list.txt', 'w')
    json.dump(nyc_events, f, indent=4)
