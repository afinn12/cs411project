import requests
from ..locations import googlemaps_key
# import googlemaps_key
import json
import os
import networkx as nx

GOOGLEMAPS_API_KEY = googlemaps_key.googlemaps_key

GOOGLEMAPS_DIRECTIONS_API_ENDPOINT = 'https://maps.googleapis.com/maps/api/directions/json'

# reformat route data to be compatible with the Directions Renderer on the frontend
def reformat_route_data(data):
    # change lat-long bounds
    for route in data['routes']:
        new_bounds = {
            "east": route['bounds']["northeast"]["lng"],
            "north": route['bounds']["northeast"]["lat"],
            "west": route['bounds']["southwest"]["lng"],
            "south": route['bounds']["southwest"]["lat"]
        }
        route['bounds'] = new_bounds
    
    # change html_instructions to instructions
    def rename_fields(data, old_name, new_name):
        if isinstance(data, dict):
            for key, value in list(data.items()):
                if key == old_name:
                    data[new_name] = data.pop(key)
                elif isinstance(value, (list, dict)):
                    rename_fields(value, old_name, new_name)
        elif isinstance(data, list):
            for item in data:
                rename_fields(item, old_name, new_name)
        
    rename_fields(data, "html_instructions", "instructions")

    

# use the Routes API to get a route from origin to destination
# origin and destination are names of cities in the list of 100
# returns a JSON
def get_direct_route(origin, destination):
    route_args = {
        'origin': origin,
        'destination': destination,
        'travelMode': 'DRIVING',
        'key': GOOGLEMAPS_API_KEY
    }
    response = requests.get(GOOGLEMAPS_DIRECTIONS_API_ENDPOINT, params=route_args)
    data = response.json()

    if response.status_code == 200 and data['status'] == 'OK':
        request_data = {
            'request': {
                'origin': origin, 
                'destination': destination,
                'travelMode': 'DRIVING'
            }
        }
        reformat_route_data(data)
        return data | request_data
    else:
        print(f"Error: {response.status_code} - {data.get('error_message', 'Unknown error')}")
        print(data)


# compute suitable split points along the route so that the number of legs < distance_limit is minimized
# also include the destination as a point
# route is a route computed by get_route: it should contain just 1 leg
# distance_limit is in miles
# returns a list of tuples of lat-long coordinates
def compute_split_points_on_daily_limit(route, distance_limit):
    # extract the list of steps
    steps = route['routes'][0]['legs'][0]['steps']
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

    split_points.append((steps[-1]['end_location']['lat'], steps[-1]['end_location']['lng']))
    return split_points


# compute the shortest path from irigin to destination, only traversing the graph of 100 cities,
# not allowing edges with distance greater than the daily limit
# also include the destination as a point
# origin and destination are names of cities in the list of 100
# return a list of tuples of lat-long coordinates for each split city (each city in between the ends)
def get_city_route(origin, destination, distance_limit):
    # load the adj_list JSON file
    curr_dir = os.path.dirname(__file__)
    adj_list_file_path = os.path.join(curr_dir, '100cities/100cities_closest_n_adj_list.json')
    adj_list = json.load(open(adj_list_file_path))

    # make the nx Graph, exluding any edge longer than the distance_limit
    G = nx.Graph()
    for city1 in adj_list:
        for entry in adj_list[city1]:
            city2 = entry['name']
            if entry['distanceInMeters'] <= distance_limit * 1609:
                G.add_edge(city1, city2, weight=entry['distanceInMeters'])
    
    if origin in G and destination in G and nx.has_path(G, origin, destination):
        path = nx.shortest_path(G, origin, destination)
        # print(path)
        split_cities = path[1:]
        distance_matrix_file_path = os.path.join(curr_dir, '100cities/DistanceMatrix.json')
        distance_matrix = json.load(open(distance_matrix_file_path))
        city_name_to_index = distance_matrix['index']
        city_index_to_info = distance_matrix['cities']

        split_points = [
            (city_index_to_info[city_name_to_index[city]]['lat'],
            city_index_to_info[city_name_to_index[city]]['long'])
            for city in split_cities
        ]

        return split_points
    
    else:
        print('No path between {} and {}; try using a larger distance limit'.format(origin, destination))
        return []
    

# use the Routes API to get a route from origin to destination, taking the stops into account
# origin and destination are names of cities in the list of 100
# stops should be a list of lat-longs, i.e. the coordinates of hotels
def get_route_with_stops(origin, destination, stops):
    route_args = {
        'origin': origin,
        'destination': destination,
        'waypoints': '|'.join(map(lambda x: f'{x[0]},{x[1]}', stops)),
        'travelMode': 'DRIVING',
        'key': GOOGLEMAPS_API_KEY
    }
    response = requests.get(GOOGLEMAPS_DIRECTIONS_API_ENDPOINT, params=route_args)
    data = response.json()

    if response.status_code == 200 and data['status'] == 'OK':
        request_data = {
            'request': {
                'origin': origin, 
                'destination': destination,
                'travelMode': 'DRIVING'
            }
        }
        reformat_route_data(data)
        return data | request_data
    else:
        print(f"Error: {response.status_code} - {data.get('error_message', 'Unknown error')}")
        print(data)


# test the functionality with lat-longs
if __name__ == '__main__':
    nyc = 'New York, NY'
    boston = 'Boston, MA'
    la = 'Los Angeles, CA'
    miami = "Miami, FL"

    # f = open('sample_route.txt', 'w')
    # route = get_direct_route(nyc, boston)
    # json.dump(route, f)

    # split_points = compute_split_points_on_daily_limit(route, 100)
    # new_route = get_route_with_stops(nyc, boston, split_points)
    nyc_miami_split_cities = get_city_route(nyc, miami, 500)
    new_route = get_route_with_stops(nyc, miami, nyc_miami_split_cities)

    f = open('sample_route_with_stops.txt', 'w')
    json.dump(new_route, f, indent=4)
    
    