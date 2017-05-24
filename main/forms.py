from django import forms

class ServiceForm(forms.Form):
    dropoff = forms.CharField(max_length=100)
    pickup = forms.CharField(max_length=100)
    mechanic = forms.CharField(max_length=50)
    repair_type = forms.CharField(max_length=10)
