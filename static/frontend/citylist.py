import json

# Read JSON data from file
with open('cities.json', 'r') as file:
    data = json.load(file)

# Extract unique names
unique_names = []
cities = []

for city in data:
    city_data = data[city]
    for entry in city_data:
        if entry['name'] not in unique_names:
            unique_names.append(entry['name'])
            city_name = entry['name'].split(',')[0].strip()  # Split and get the first part
            cities.append(city_name)
            


unique_names=sorted(unique_names)

for i in range(len(unique_names)):
    print(f"<option value=\"{unique_names[i]}\">{unique_names[i]}</option>")

