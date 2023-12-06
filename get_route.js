const fs = require('fs');

fs.readFile('locations/sample_city_roadtrip.txt', 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading the file:', err);
    return;
  }
  try {
    const jsonData = JSON.parse(data);
    console.log(jsonData);
  } catch (parseErr) {
    console.error('Error parsing JSON:', parseErr);
  }
});
