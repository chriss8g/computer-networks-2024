# En tu aplicación Django, en forms.py
from django import forms

class HTTPRequestForm(forms.Form):
    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    ]

    method = forms.ChoiceField(choices=METHOD_CHOICES, label='Method')
    host = forms.CharField(label='Host', max_length=100)
    port = forms.IntegerField(label='Port')
    resource = forms.CharField(label='Resource', max_length=100)
    data = forms.CharField(label='Data', required=False, widget=forms.Textarea)
