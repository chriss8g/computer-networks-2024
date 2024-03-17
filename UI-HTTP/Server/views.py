# En views.py
from django.shortcuts import render


def ServerPageView(request):
    
    return render(request, 'server.html')
