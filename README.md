# Roadtrip Planner

## Project structure
- cs411project: project-scope (google oauth, login/logout/home directories)
- cs411project_app: app-scope
    - locations: handles API calling and logic for choosing split points / hotels / events
    - static: JS files for certain API calls
    - templates: HTML files
- There are also several sample output files that were used during development

## Backend
- Python Django
- Make API requests to Google Maps,  Amadeus (Hotels), Yelp (Events)
- OAuth2 with Google
- Give 4 routes
    - Direct Route: get from city A to B as directly as possible
    - City-Based Route: get from A to B going through some cities in between
        - Both cities have to be one of the 100 largest US cities (actually 98 cities, excluding Honolulu and Anchorage, but including some Canada cities like Toronto and Vancouver) for this kind of route
    - Each of these routes can have a "close" or "cheap" option for hotels
- For hotels:
    - Determine split points 
        - For the direct route, this is based on just a daily distance limit
        - For the city based route, the cities are the split points, meaning hotels must be in one of the 100 cities. This must also obey the daily distance limit
    - For each split point:
        - If "close," choose the closest hotel
        - If "cheap," choose the cheapest from the closest 10
- Find events around each split point

## Frontend
- JS, HTML, etc.
- Login with Google
- Home page: get a new roadtrip, or view a previously saved roadtrip
- Input starting and ending city, daily distance limit, and the departure date
- Wait for the loading, and make a direct/city choice plus a cheap/close hotel choice
- Save button: write to DB

## DB
- SQL
- Route data is a JSON; store email, origin, destination, and data_created with the route data on DB