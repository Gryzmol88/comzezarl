//Dynamiczne ładowanie listy miast po wybraniu kraju
$(document).ready(function () {

        //TODO Po wpisaniu kraju, niech będzie od razu wybrany z listy tak samo z miastem
        const countrySelect = $("#country-select");
        const citySelect = $("#city-select");
        const addCityBtn = $("#add-city-btn");



    countrySelect.change(function () {
        const countryId = $(this).val(); // Pobieramy ID wybranego kraju

        // Wyczyść listę miast
        citySelect.empty();
        citySelect.append('<option value="">-- Wybierz miasto --</option>');


        // Jeśli nie wybrano kraju, wyłącz listę miast
        if (!countryId) {
            citySelect.prop("disabled", true);
            addCityBtn.prop("disabled", true);

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
                addCityBtn.prop("disabled", false);
            },
            error: function () {
                alert("Wystąpił błąd podczas ładowania miast.");
            }
        });
    });
});

//Dynamiczne dodawanie nowego kraju do bazy danych
document.addEventListener("DOMContentLoaded", function () {
    const addCountryButton = document.getElementById("add-country-btn");

    if (addCountryButton) {
        addCountryButton.addEventListener("click", function () {
            const url = addCountryButton.getAttribute("data-url");

            fetch(url)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Błąd podczas ładowania modala.");
                    }
                    return response.text();
                })
                .then((html) => {
                    // Dodaj modal do DOM
                    const modalContainer = document.createElement("div");
                    modalContainer.innerHTML = html;
                    document.body.appendChild(modalContainer);

                    // Pokaż modal
                    const modal = new bootstrap.Modal(modalContainer.querySelector(".modal"));
                    modal.show();

                    // Obsługa kliknięcia przycisku "Zapisz"
                    const saveButton = modalContainer.querySelector("#saveCountryButton");
                    saveButton.addEventListener("click", function () {
                        const countryName = modalContainer.querySelector("#newCountryName").value;

                        if (!countryName) {
                            modalContainer.querySelector("#addCountryError").classList.remove("d-none");
                            return;
                        }

                        // Wyślij dane do serwera (AJAX)
                        fetch(saveButton.getAttribute("data-url"), {  // Zmieniony URL
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "X-CSRFToken": getCookie("csrftoken"), // Upewnij się, że csrf jest poprawnie ustawione
                            },
                            body: JSON.stringify({
                                name: countryName
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                modal.hide();
                            } else {
                                modalContainer.querySelector("#addCountryError").classList.remove("d-none");
                            }
                        })
                        .catch(error => {
                            console.error("Błąd przy dodawaniu kraju:", error);
                            alert("Błąd przy dodawaniu kraju.");
                        });
                    });

                    // Usuń modal z DOM po jego zamknięciu
                    modalContainer.querySelector(".modal").addEventListener("hidden.bs.modal", function () {
                        modalContainer.remove();
                    });
                })
                .catch((error) => {
                    console.error("Nie udało się załadować modala:", error);
                    alert("Nie udało się załadować modala.");
                });
        })
    }
});


//Dynamiczne dodawanie nowego miasta do bazy danych
document.addEventListener("DOMContentLoaded", function () {
    const addCityButton = document.getElementById("add-city-btn");

    if (addCityButton) {
        addCityButton.addEventListener("click", function () {
            const url = addCityButton.getAttribute("data-url");


            let countryId = $("#country-select").val(); // Pobiera wartość pola Country


            fetch(url)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Błąd podczas ładowania modala.");
                    }
                    return response.text();
                })
                .then((html) => {
                    // Dodaj modal do DOM
                    const modalContainer = document.createElement("div");
                    modalContainer.innerHTML = html;
                    document.body.appendChild(modalContainer);

                    // Pokaż modal
                    const modal = new bootstrap.Modal(modalContainer.querySelector(".modal"));
                    modal.show();

                    // Obsługa kliknięcia przycisku "Zapisz"
                    const saveButton = modalContainer.querySelector("#saveCityButton");
                    saveButton.addEventListener("click", function () {
                        const cityName = modalContainer.querySelector("#newCityName").value;

                        if (!cityName) {
                            modalContainer.querySelector("#addCityError").classList.remove("d-none");
                            return;
                        }

                        // Wyślij dane do serwera (AJAX)
                        fetch(saveButton.getAttribute("data-url"), {  // Zmieniony URL
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "X-CSRFToken": getCookie("csrftoken"), // Upewnij się, że csrf jest poprawnie ustawione
                            },
                            body: JSON.stringify({
                                cityName: cityName,
                                countryId: countryId
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                modal.hide();
                            } else {
                                modalContainer.querySelector("#addCityError").classList.remove("d-none");
                            }
                        })
                        .catch(error => {
                            console.error("Błąd przy dodawaniu miasta:", error);
                            alert("Błąd przy dodawaniu miasta.");
                        });
                    });

                    // Usuń modal z DOM po jego zamknięciu
                    modalContainer.querySelector(".modal").addEventListener("hidden.bs.modal", function () {
                        modalContainer.remove();
                    });
                })
                .catch((error) => {
                    console.error("Nie udało się załadować modala:", error);
                    alert("Nie udało się załadować modala.");
                });
        });
    }
});

// Funkcja do pobierania tokenu CSRF z ciasteczek
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
