from django import forms
from .models import Country, Restaurant

class PostForm(forms.Form):
    existing_country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        empty_label="Wybierz kraj",
        label='Istniejący kraj',
    )
    restaurant = forms.ModelChoiceField(
        queryset=Restaurant.objects.none(),  # Domyślnie puste
        required=False,
        empty_label="Wybierz restaurację",
        label='Restauracja',
    )

