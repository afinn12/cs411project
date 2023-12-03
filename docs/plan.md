# Plan

## Backend
- Local
- Python Django
- HTTP Server
- Make API requests to Google Maps, Hotels (Amadeus), Events (Yelp)
- OAuth (Google probably)
- Communicate with Mongo server for user info
- Get two cities from frontend &rarr; give 4 routes
    - Direct Route: get from city A to B as directly as possible
    - City-Based Route: get from A to B going through some cities in between
        - Both cities have to be one of the 100 largest US cities (actually 98 cities, excluding Honolulu and Anchorage, but including some Canada cities like Toronto and Vancouver) for this kind of route (maybe add this restriction to the direct route as well)
    - Each of these routes can have a "close" or "cheap" option for hotels
- For hotels:
    - Determine split points 
        - For the direct route, this is based on a daily distance limit
        - For the city based route, the cities are the split points, meaning hotels must be in one of the 100 cities
    - For each split point:
        - If "close," choose the closest hotel
        - If "cheap," choose the cheapest from the closest 10
- Find events around each split point
- Give route, hotels, events to front end
- Store the computed route on DB

## Frontend
- Give 2 cities to backend, and receive:
    - Direct route and city based route
    - Each route has their corresponding hotels, and events around them
- Ask to save the route, can delete routes

## DB
- Also local
- Mongo
- Route data is a JSON, so just stick userID, username, and createDate with the route