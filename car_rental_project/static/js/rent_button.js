document.addEventListener('DOMContentLoaded', function() {
    // Find all elements with the class 'rent-button'
    const rentButtons = document.querySelectorAll('.rent-button');

    // Attach click event listener to each button
    rentButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            // Get the car_id directly from the button's data attribute
            const carId = button.dataset.carId;

            // Construct the rentUrl using the carId
            const rentUrl = "{% url 'car_rent' car_id=0 %}".replace('0', carId);

            // Perform further actions with carId or rentUrl
            windows.location.href = rentUrl
        });
    });
});
