# En views.py
from django.shortcuts import render
from .server import run_server
from threading import Thread


def ServerPageView(request):
    try:
        client_handler = Thread(target=run_server)
        client_handler.start()
    except error:
        print(e)
        
    return render(request, 'server.html')
