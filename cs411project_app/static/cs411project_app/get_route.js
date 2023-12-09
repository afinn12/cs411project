function get_sample_roadtrip_output() {
  const apikey_endpoint = 'http://127.0.0.1:8000/cs411project_app/get_sample_roadtrip/';
  const post_request_options = {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
  };

  // Use fetch to make an HTTP request
  return fetch(apikey_endpoint, post_request_options)
      .then(response => response.json())
      .then(data => {
          return data;
      })
      .catch(err => {
          console.error('Error reading the file:', err);
          throw err;
      });
}

// Example usage
// get_sample_roadtrip_output()
//   .then(data => {
//       console.log(data);
//       // Optionally, you can create the script element here if needed
//   })
//   .catch(error => {
//       console.error('Error:', error);
//   });
