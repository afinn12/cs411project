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

function get_roadtrip_output(origin, destination, is_direct_route, distance_limit, start_date) {
    const apikey_endpoint = 'http://127.0.0.1:8000/cs411project_app/get_roadtrip/';
    const data = {
        'origin': origin,
        'destination': destination,
        'is_direct_route': is_direct_route,
        'distance_limit': distance_limit,
        'start_date': start_date
    }
    const post_request_options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    };
    return fetch(apikey_endpoint, post_request_options)
        .then(response => response.json())
        .then(data => {
            return data;
        })
        .catch(err => {
            console.error('Error making the API call:', err);
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
