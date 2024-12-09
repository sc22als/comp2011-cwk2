$(document).ready(function(event) {
    $('.add-ingredient').click(function(event) {
        event.preventDefault();  // Prevent form submission

        var ingredientName = $('#ingredient-inputs input[name="ingredient"]').val(); // Get the value of the input

        // Capitalize the first letter and make the rest lowercase
        ingredientName = ingredientName.charAt(0).toUpperCase() + ingredientName.slice(1).toLowerCase();

        if (ingredientName) {  // Check if ingredientName isn't empty
            $.ajax({
                url: '/add-recipe',  // Flask route
                type: 'POST',
                data: {
                    ingredient: ingredientName
                },
                contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
                success: function(data) {
                    if (data.success) {
                        $('#ingredientSuccess').text(data.success).show();
                        $('#ingredientError').hide();
                        $('#ingredientInfo').hide();
                    } else if (data.info) {
                        $('#ingredientInfo').text(data.info).show();
                        $('#ingredientSuccess').hide();
                        $('#ingredientError').hide();
                    }
                },
                error: function(xhr, status, error) {
                    $('#ingredientError').text('Error: ' + error).show();
                    $('#ingredientSuccess').hide();
                    $('#ingredientInfo').hide();
                }
            });
        } else {
            $('#ingredientInfo').text('Please provide an ingredient.').show();
            $('#ingredientSuccess').hide();
            $('#ingredientError').hide();
        }
    });
    
    // $('.add-ingredient').click(function() {
    //     console.log('Button clicked!');
    //     var ingredientName = $('#ingredient-inputs input[name="ingredient"]').val(); // Get the value of the input
    //     console.log(ingredientName);

    //     // Capitalize the first letter and make the rest lowercase
    //     ingredientName = ingredientName.charAt(0).toUpperCase() + ingredientName.slice(1).toLowerCase();

    //     console.log(ingredientName);
    // });
});

