# Plan

## Backend
- Python Django
- HTTP Server
- Make API requests to Google Maps, Hotels, Events (Amadeus, Yelp?)
- OAuth (Google probably)
- Communicate with MySQL server for user info
- Get two cities from frontend &rarr; ask Google Maps for the route
- For hotels:
    - Determine starting points (user input or otherwise)
    - For each starting point, choose 1 hotel around it
        - For fastest route, get closet hotel
        - For cheapest route, choose the cheapest from the closest 10
- Recompute the route given these hotels
- Find restaurants around each hotel
- Give route, hotels, restaurants to front end
- Store the computed route on DB

## Frontend
- Give 2 cities to backend, and receive:
    - Fastest route and cheapest route
    - Each route has their corresponding hotels, and restaurants around them
- Ask to save the route, can delete routes

## DB
- MySQL on AWS (?)
- userID, etc.
- route, createDate