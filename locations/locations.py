import events
import hotels
import maps
import json

HOTEL_SEARCH_RADIUS = 10
EVENT_SEARCH_RADIUS = 10
DAILY_DISTANCE_LIMIT_MILES = 100

# combine the 3 APIs to get a roudtrip plan
# origin and detination are tuples of lat-long coordinates
# fast_flag is a bool flag to indicate if this is the "fast" route or "cheaper" route
# return a JSON
def get_roadtrip(origin, destination, fast_flag=True):
    # get the route and split points
    route = maps.get_route(origin, destination)
    split_points = maps.compute_split_points_on_daily_limit(route, DAILY_DISTANCE_LIMIT_MILES * 1609)


    # find hotels around each split point
    amadeus_token = hotels.get_amadeus_access_token()
    hotel_list_per_point = [
        hotels.get_hotels_around_point(amadeus_token, x, y, HOTEL_SEARCH_RADIUS) for x,y in split_points
    ]

    hotel_per_point_fast = []
    hotel_per_point_cheap = []

    # for each split point, pick one hotel to stay at based on if the route is fast or cheap
    for i in range(len(hotel_list_per_point)):
        hotel_list = hotel_list_per_point[i]
        hotel_list_array = [(hotel_list[hotel], hotel) for hotel in hotel_list]
        hotel_list_array.sort(key=lambda info_hotel_pair: info_hotel_pair[0]['distance'])
        
        # choose closest hotel and add it to the list for fast hotels
        hotel_choice_info, hotel_choice_id = hotel_list_array[0]
        hotel_per_point_fast.append((hotel_choice_id, hotel_choice_info))

        # choose cheapest from closet 10 hotels and add it to the list for cheap hotels
        hotel_list_array = hotel_list_array[:10]
        hotel_list_array.sort(key=lambda info_hotel_pair: info_hotel_pair[0]['price']['total'])
        hotel_choice_info, hotel_choice_id = hotel_list_array[0]
        hotel_per_point_cheap.append((hotel_choice_id, hotel_choice_info))


    # find events around each split point
    event_list_per_point = [
        events.get_events_around_point(x, y, EVENT_SEARCH_RADIUS) for x,y in split_points
    ]


    # recompute the route based on the fast hotels
    stops_fast = []
    for hotel_id, hotel_info in hotel_per_point_fast:
        stops_fast.append((hotel_info['latitude'], hotel_info['longitude']))
    new_route_fast = maps.get_route_with_stops(origin, destination, stops_fast)


    # recompute the route based on the cheap hotels
    stops_cheap = []
    for hotel_id, hotel_info in hotel_per_point_cheap:
        stops_cheap.append((hotel_info['latitude'], hotel_info['longitude']))
    new_route_cheap = maps.get_route_with_stops(origin, destination, stops_cheap)


    # format the return json
    roadtrip_info_fast = {
        'route': new_route_fast,
        'hotels': [id_info_pair[1] for id_info_pair in hotel_per_point_fast],
        'events': event_list_per_point
    }
    roadtrip_info_cheap = {
        'route': new_route_cheap,
        'hotels': [id_info_pair[1] for id_info_pair in hotel_per_point_cheap],
        'events': event_list_per_point
    }

    return {
        'close_hotel_route': roadtrip_info_fast,
        'cheap_hotel_route': roadtrip_info_cheap
    }


# test the functionality on the lat-longs for NYC and Boston
if __name__ == '__main__':
    # nyc coors
    nyc = 40.7128, -74.0060
    # boston coors
    boston = 42.3601, -71.0589

    f = open('sample_roadtrip.txt', 'w')
    roadtrip = get_roadtrip(nyc, boston)
    json.dump(roadtrip, f, indent=4)
