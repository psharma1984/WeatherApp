from django import forms


class LocationSearchForm(forms.Form):
    keyword = forms.CharField(label="Keyword", max_length=100)
