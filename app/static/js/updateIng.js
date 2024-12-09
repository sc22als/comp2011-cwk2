$(document).ready(function() {
    // store all selected ingredients
    var selectedIngredients = [];

    // Function to update the ingredient list dynamically
    function updateIngredientList() {
        $.ajax({
            url: '/get-ingredients',  // Flask route to get updated ingredients
            type: 'GET',
            success: function(data) {
                var ingredientSelect = $('#ingredient-select');
                ingredientSelect.empty();  // Clear  current options

                // Add a default option to the dropdown
                ingredientSelect.append('<option value="">Select an ingredient</option>');

                // Add each ingredient to the dropdown
                data.ingredient_list.forEach(function(ingredient) {
                    ingredientSelect.append('<option value="' + ingredient + '">' + ingredient + '</option>');
                });
            },
            error: function(xhr, status, error) {
                alert('Error refreshing ingredient list');
            }
        });
    }

    // when the page is ready to populate the initial list
    updateIngredientList();

    $('#refreshIngredients').click(function() {
        updateIngredientList();
    });

    // Handle select change
    $('#ingredient-select').change(function() {
        var selectedIngredient = $(this).val();

        if (selectedIngredient && !selectedIngredients.includes(selectedIngredient)) {
            // Add the ingredient to the array if not already selected
            selectedIngredients.push(selectedIngredient);

            displaySelectedIngredients();
            console.log("selected ingredients array: " + selectedIngredients)
        }
    });

    // display all selected ingredients in a comma-separated list
    function displaySelectedIngredients() {
        $('#list-ingredients-selected').text('Selected Ingredients: ' + selectedIngredients.join(', '));
        // Update the hidden input field with the selected ingredients (comma-separated)
        $('#selected-ingredients').val(selectedIngredients.join(','));
    }
});
