$(document).ready(function () {
    $("#country-select").change(function () {
        const countryId = $(this).val(); // Pobieramy ID wybranego kraju
        const citySelect = $("#city-select");

        // Wyczyść listę miast
        citySelect.empty();
        citySelect.append('<option value="">-- Wybierz miasto --</option>');

        // Jeśli nie wybrano kraju, wyłącz listę miast
        if (!countryId) {
            citySelect.prop("disabled", true);
            return;
        }

        // Wysyłamy żądanie AJAX do widoku Django
        $.ajax({
            url: `/newpost/${countryId}/cities/`,
            method: "GET",
            success: function (response) {
                const cities = response.cities;

                // Jeśli brak miast w odpowiedzi
                if (cities.length === 0) {
                    citySelect.append('<option value="">Brak miast w tym kraju</option>');
                } else {
                    // Dodaj miasta do rozwijanej listy
                    cities.forEach(city => {
                        citySelect.append(`<option value="${city.id}">${city.name}</option>`);
                    });
                }

                // Włącz listę miast
                citySelect.prop("disabled", false);
            },
            error: function () {
                alert("Wystąpił błąd podczas ładowania miast.");
            }
        });
    });
});