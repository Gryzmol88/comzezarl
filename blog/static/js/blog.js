  $(document).ready(function () {
            $('#country').change(function () {
                const countryId = $(this).val();
                const citySelect = $('#city');

                if (countryId) {
                    $.ajax({
                        url: `/get-cities/${countryId}/`, // URL endpoint do widoku
                        method: 'GET',
                        success: function (data) {
                            citySelect.empty().append('<option value="">--- Select a city ---</option>');
                            data.forEach(function (city) {
                                citySelect.append(`<option value="${city.id}">${city.name}</option>`);
                            });
                            citySelect.prop('disabled', false);
                        },
                        error: function () {
                            alert('An error occurred while fetching cities.');
                        }
                    });
                } else {
                    citySelect.empty().append('<option value="">--- Select a city ---</option>');
                    citySelect.prop('disabled', true);
                }
            });
        });