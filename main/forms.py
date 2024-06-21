from django import forms


class SubscribeForm(forms.Form):
    email =forms.EmailField()
    nombre=forms.CharField()
    password=forms.CharField()
    
