function get_google_apikey() {
  const apikey_endpoint = 'http://127.0.0.1:8000/cs411project_app/get_google_apikey/';
  const post_request_options = {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
  };

  // Use fetch to make an HTTP request
  return fetch(apikey_endpoint, post_request_options)
      .then(response => response.text())
      .then(data => {
        //   console.log(data);
          return data.substring(1, data.length - 1);
      })
      .catch(err => {
          console.error('Error reading the file:', err);
          throw err;
      });
}

function get_google_directions_link() {
  return get_google_apikey()
      .then(apikey => {
          return "https://maps.googleapis.com/maps/api/js?key=" + apikey + "&callback=initMap&v=weekly";
      })
      .catch(error => {
          console.error('Error getting API key:', error);
          throw error;
      });
}

// Example usage
// get_google_directions_link()
//   .then(apikey => {
//       console.log('Link with API key:', apikey);
//       // Optionally, you can create the script element here if needed
//   })
//   .catch(error => {
//       console.error('Error:', error);
//   });
