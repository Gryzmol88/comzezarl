from django import forms

class PostForm(forms.Form):
    name = forms.CharField(max_length=250)
    email = forms.EmailField()
