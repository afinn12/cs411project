from ..locations import events
from ..locations import hotels
from ..locations import maps
# import events
# import hotels
# import maps
import json
import datetime

HOTEL_SEARCH_RADIUS = 25
EVENT_SEARCH_RADIUS = 20   

# combine the 3 APIs to get a roudtrip plan
# origin and destination are names of cities in the list of 100
# is_direct_route is a boolean for if the returned route should be direct (True) or city-based (False)
# distance_limit is the daily distance limit in miles
# start_date is a date in YYYY-MM-DD format
# return a JSON
def get_roadtrip(origin, destination, is_direct_route, distance_limit, start_date):
    ret = {}

    # get the route and split points
    if is_direct_route:
        route = maps.get_direct_route(origin, destination)
        split_points = maps.compute_split_points_on_daily_limit(route, distance_limit)
    else:
        split_points = maps.get_city_route(origin, destination, distance_limit)


    # find hotels around each split point
    amadeus_token = hotels.get_amadeus_access_token()
    start_date = datetime.date.fromisoformat(start_date)
    # for the direct route, you check in to a hotel on a day, and then check out the next day
    if is_direct_route:
        hotel_list_per_point = [
            hotels.get_hotels_around_point(amadeus_token, x, y, HOTEL_SEARCH_RADIUS, 
                                            start_date + datetime.timedelta(days=i),
                                            start_date + datetime.timedelta(days=i+1)) 
            for i,(x,y) in enumerate(split_points)
        ]
    # for the city route, you check in to a hotel on a day, and then check out 2 days after
    else:
        hotel_list_per_point = [
            hotels.get_hotels_around_point(amadeus_token, x, y, HOTEL_SEARCH_RADIUS, 
                                            start_date + datetime.timedelta(days=2*i),
                                            start_date + datetime.timedelta(days=2*(i+1))) 
            for i,(x,y) in enumerate(split_points)
        ]

    hotel_per_point_fast = []
    hotel_per_point_cheap = []

    # for each split point, pick one hotel to stay at based on if the route is fast or cheap
    for i in range(len(hotel_list_per_point)):
        hotel_list = hotel_list_per_point[i]
        hotel_list_array = [(hotel_list[hotel], hotel) for hotel in hotel_list]
        hotel_list_array.sort(key=lambda info_hotel_pair: info_hotel_pair[0]['distance'])
        
        # choose closest hotel and add it to the list for fast hotels
        hotel_choice_info, hotel_choice_id = hotel_list_array[0] if hotel_list_array else (None, None)
        hotel_per_point_fast.append((hotel_choice_id, hotel_choice_info))

        # choose cheapest from closet 10 hotels and add it to the list for cheap hotels
        hotel_list_array = hotel_list_array[:10]
        hotel_list_array.sort(key=lambda info_hotel_pair: info_hotel_pair[0]['price']['total'])
        hotel_choice_info, hotel_choice_id = hotel_list_array[0] if hotel_list_array else (None, None)
        hotel_per_point_cheap.append((hotel_choice_id, hotel_choice_info))


    # find events around each split point
    # the start and end date used for the events are one week before and one week after the "event-day"
    # for the direct route, the "event-day" for a split point is the same day as the check in date for the hotel
    if is_direct_route:
        event_list_per_point = [
            events.get_events_around_point(x, y, EVENT_SEARCH_RADIUS, 
                                           start_date + datetime.timedelta(days=i-7),
                                           start_date + datetime.timedelta(days=i+7)) 
            for i,(x,y) in enumerate(split_points)
        ]
    # for the city route, the "event-day" for a split point is the day after the check in date for the hotel
    else:
        event_list_per_point = [
            events.get_events_around_point(x, y, EVENT_SEARCH_RADIUS,
                                           start_date + datetime.timedelta(days=2*i+1 - 7),
                                           start_date + datetime.timedelta(days=2*i+1 + 7)) 
            for i,(x,y) in enumerate(split_points)
        ]


    # print(hotel_per_point_fast)

    # recompute the route based on the fast hotels
    stops_fast = []
    for i, (hotel_id, hotel_info) in enumerate(hotel_per_point_fast):
        stops_fast.append((hotel_info['latitude'], hotel_info['longitude']) if hotel_id else split_points[i])
    new_route_fast = maps.get_route_with_stops(origin, destination, split_points)


    # recompute the route based on the cheap hotels
    stops_cheap = []
    for i, (hotel_id, hotel_info) in enumerate(hotel_per_point_cheap):
        stops_cheap.append((hotel_info['latitude'], hotel_info['longitude']) if hotel_id else split_points[i])
    new_route_cheap = maps.get_route_with_stops(origin, destination, split_points)


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
    
    ret['close_hotel_route'] = roadtrip_info_fast
    ret['cheap_hotel_route'] = roadtrip_info_cheap
    
    return ret


# test the functionality on the lat-longs for NYC and Miami
if __name__ == '__main__':
    nyc = 'New York, NY'
    boston = 'Boston, MA'
    miami = 'Miami, FL'

    # f = open('sample_direct_roadtrip.txt', 'w')
    # roadtrip = get_roadtrip(nyc, boston, True, 100, '2023-12-15')
    # json.dump(roadtrip, f, indent=4)

    f = open('sample_city_roadtrip.txt', 'w')
    roadtrip = get_roadtrip(nyc, miami, False, 500, '2024-01-15')
    json.dump(roadtrip, f, indent=4)
