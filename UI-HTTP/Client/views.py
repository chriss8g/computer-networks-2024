# En views.py
from django.shortcuts import render
from .forms import HTTPRequestForm
from .http import send_request
import json


def HomePageView(request):
    if request.method == 'POST':
        form = HTTPRequestForm(request.POST)
        if form.is_valid():
            # Obtén los datos del formulario
            method = form.cleaned_data['method']
            host = form.cleaned_data['host']
            port = form.cleaned_data['port']
            resource = form.cleaned_data['resource']
            data = form.cleaned_data['data']

            status, body, headers = "", "", ""
            # Envia la solicitud HTTP utilizando la función existente
            try:
                status, body, headers = send_request(host, port, method, resource, data)
                if(is_valid_json(body) and method in ["GET", "POST", "PUT", "OPTIONS"]):
                    json_obj = json.loads(body)
                    body = json.dumps(json_obj, indent=4, sort_keys=True)
            except Exception as e:
                status = f"Error: {str(e)}"

            return render(request, 'home.html', {'form': form, 'status': status, 'body': body, 'headers': headers.split('\r\n')})
    else:
        form = HTTPRequestForm()

    return render(request, 'home.html', {'form': form, 'status': None})

def is_valid_json(text):
    try:
        json.loads(text)
        return True
    except ValueError:
        return False