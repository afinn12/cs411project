import requests


url = 'https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-geocode?latitude=40.7128&longitude=-74.0060&radiusUnit=5&hotelSource=ALL'

response = requests.get(url)

print(response.json())
