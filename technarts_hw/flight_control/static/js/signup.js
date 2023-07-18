$(document).ready(function() {
    $('#signup_submit').click(function(e) {
        e.preventDefault();
        
        // Retrieve the values from the input fields
        var username = $('#username').val();
        var password = $('#password').val();
        
        // Create the request data
        var data = {
            'username': username,
            'password': password
        };
        
        // Send the POST request
        $.ajax({
            url: '/signup/',
            type: 'POST',
            data: data,
            success: function(response) {
                // Handle the success response
                if (response.token) {
                    // Store the JWT token in localStorage
                    localStorage.setItem('token', response.token);
                    // Redirect to the home page
                    window.location.href = '/home/';
                } else {
                    console.log('Token not found in the response.');
                }
            },
            error: function(xhr, status, error) {
                // Handle the error response
                console.log(xhr.responseText);
            }
        });
    });
});
