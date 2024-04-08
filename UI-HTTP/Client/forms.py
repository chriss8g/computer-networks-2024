# En tu aplicación Django, en forms.py
from django import forms

class HTTPRequestForm(forms.Form):
    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('HEAD', 'HEAD'),
        ('CONNECT', 'CONNECT'),
        ('OPTIONS', 'OPTIONS'),
    ]
   
    method = forms.ChoiceField(choices=METHOD_CHOICES, label='Method')
    url = forms.CharField(label='URL', max_length=500, widget=forms.TextInput(attrs={'class': 'form-control', "style" : "width : 500px"}))
    data = forms.CharField(label='Data', required=False, widget=forms.Textarea(attrs={'class': 'form-control', "style" : "height : 100px"}))
