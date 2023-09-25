from django import forms


class LocationSearchForm(forms.Form):
    choices = (("metric", "C"), ("imperial", "F"))
    keyword = forms.CharField(label="Keyword", max_length=100)
    units = forms.ChoiceField(choices=choices, widget=forms.Select())
