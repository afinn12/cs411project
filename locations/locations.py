import events
import hotels
import maps
import json

HOTEL_SEARCH_RADIUS = 10
EVENT_SEARCH_RADIUS = 10
DAILY_DISTANCE_LIMIT_MILES = 100

# origin and detination: tuples of lat-longs
# fast_flag: flag to indicate if this is the "fast" route or "cheaper" route
def get_roadtrip(origin, destination, fast_flag=True):
    # get the route and split points
    route = maps.get_route(origin, destination)
    split_points = maps.compute_split_points_on_daily_limit(route, DAILY_DISTANCE_LIMIT_MILES * 1609)


    # find hotels around each split point
    amadeus_token = hotels.get_amadeus_access_token()
    hotel_list_per_point = [
        hotels.get_hotels_around_point(amadeus_token, x, y, HOTEL_SEARCH_RADIUS) for x,y in split_points
    ]

    hotel_per_point = []
    # for each split point, pick one hotel to stay at based on if the route is fast or cheap
    for i in range(len(hotel_list_per_point)):
        hotel_list = hotel_list_per_point[i]
        hotel_list_array = [(hotel_list[hotel], hotel) for hotel in hotel_list]
        hotel_list_array.sort(key=lambda info_hotel_pair: info_hotel_pair[0]['distance'])
        # choose closest hotel
        if fast_flag:
            hotel_choice_info, hotel_choice_id = hotel_list_array[0]
        # choose cheapest from closet 10 hotels
        else:
            hotel_list_array = hotel_list_array[:10]
            hotel_list_array.sort(key=lambda info_hotel_pair: info_hotel_pair[0]['price']['total'])
            hotel_choice_info, hotel_choice_id = hotel_list_array[0]

        # add this choice to the list of hotels
        hotel_per_point.append((hotel_choice_id, hotel_choice_info))


    # find events around each split point
    event_list_per_point = [
        events.get_events_around_point(x, y, EVENT_SEARCH_RADIUS) for x,y in split_points
    ]


    # recompute the route based on the hotels
    stops = []
    for hotel_id, hotel_info in hotel_per_point:
        stops.append((hotel_info['latitude'], hotel_info['longitude']))
    new_route = maps.get_route_with_stops(origin, destination, stops)


    # format the return json
    roadtrip_info = {
        'route': new_route,
        'hotels': [id_info_pair[1] for id_info_pair in hotel_per_point],
        'events': event_list_per_point
    }

    return roadtrip_info

if __name__ == '__main__':
    # nyc coors
    nyc = 40.7128, -74.0060
    # boston coors
    boston = 42.3601, -71.0589

    f = open('sample_roadtrip.txt', 'w')
    roadtrip = get_roadtrip(nyc, boston)
    json.dump(roadtrip, f, indent=4)
