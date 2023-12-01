import requests
import googlemaps_key
import json

GOOGLEMAPS_API_KEY = googlemaps_key.googlemaps_key

GOOGLEMAPS_DIRECTIONS_API_ENDPOINT = 'https://maps.googleapis.com/maps/api/directions/json'


# use the Routes API to get a route from origin to destination
# origin and destination are tuples of lat-long coordinates
# returns a JSON
def get_route(origin, destination):
    route_args = {
        'origin': f'{origin[0]},{origin[1]}',
        'destination': f'{destination[0]},{destination[1]}',
        'key': GOOGLEMAPS_API_KEY
    }
    response = requests.get(GOOGLEMAPS_DIRECTIONS_API_ENDPOINT, params=route_args)
    data = response.json()

    if response.status_code == 200 and data['status'] == 'OK':
        return data['routes'][0]
    else:
        print(f"Error: {response.status_code} - {data.get('error_message', 'Unknown error')}")


# compute suitable split points along the route so that the number of legs < distance_limit is minimized
# route is a route computed by get_route: it should contain just 1 leg
# distance_limit is in miles
def compute_split_points_on_daily_limit(route, distance_limit):
    # extract the list of steps
    steps = route['legs'][0]['steps']
    split_points = []
    curr_distance = 0

    for step in steps:
        if curr_distance == 0:
            curr_distance += step['distance']['value']
        else:
            # does adding yourself push the distances over the threshold?
            if curr_distance+step['distance']['value']>distance_limit*1609:
                split_points.append((step['start_location']['lat'], step['start_location']['lng']))
                curr_distance = 0
            curr_distance += step['distance']['value']

    return split_points


# use the Routes API to get a route from origin to destination, taking the stops into account
# origin and destination are tuples of lat-long coordinates
# stops should be a list of lat-longs, i.e. the coordinates of hotels
def get_route_with_stops(origin, destination, stops):
    route_args = {
        'origin': f'{origin[0]},{origin[1]}',
        'destination': f'{destination[0]},{destination[1]}',
        'waypoints': '|'.join(map(lambda x: f'{x[0]},{x[1]}', stops)),
        'key': GOOGLEMAPS_API_KEY
    }
    response = requests.get(GOOGLEMAPS_DIRECTIONS_API_ENDPOINT, params=route_args)
    data = response.json()

    if response.status_code == 200 and data['status'] == 'OK':
        return data['routes'][0]
    else:
        print(f"Error: {response.status_code} - {data.get('error_message', 'Unknown error')}")


# test the functionality with lat-longs for NYC and Boston
if __name__ == '__main__':
    # nyc coors
    nyc = 40.7128, -74.0060
    # boston coors
    boston = 42.3601, -71.0589

    # f = open('sample_route.txt', 'w')
    route = get_route(nyc, boston)
    # json.dump(route, f)

    split_points = compute_split_points_on_daily_limit(route, 100)
    new_route = get_route_with_stops(nyc, boston, split_points)

    f = open('sample_route_with_stops.txt', 'w')
    json.dump(new_route, f, indent=4)
    