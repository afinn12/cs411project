import fs from 'fs';

function get_route_from_file(){
  fs.readFile('cs411project_app/locations/sample_city_roadtrip.txt', 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading the file:', err);
      return;
    }
    const JSONdata = JSON.parse(data);
    console.log(JSONdata['cheap_hotel_route']);
    return data;
  });
}

// get_route_from_file();