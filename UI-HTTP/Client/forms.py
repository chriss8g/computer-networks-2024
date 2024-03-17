# En tu aplicación Django, en forms.py
from django import forms

class HTTPRequestForm(forms.Form):
    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('HEAD', 'HEAD'),
    ]
   
    method = forms.ChoiceField(choices=METHOD_CHOICES, label='Method')
    host = forms.CharField(label='Host', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', "style" : "width : 100px"}))
    port = forms.IntegerField(label='Port', widget=forms.NumberInput(attrs={'class': 'form-control', "style" : "width : 90px"}))
    resource = forms.CharField(label='Resource', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    data = forms.CharField(label='Data', required=False, widget=forms.Textarea(attrs={'class': 'form-control', "style" : "height : 100px"}))
