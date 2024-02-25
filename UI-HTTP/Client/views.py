# En views.py
from django.shortcuts import render
from django.http import HttpResponse
from .forms import HTTPRequestForm
from .http import send_request


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

            # Envia la solicitud HTTP utilizando la función existente
            try:
                response = send_request(host, port, method, resource, data)
            except Exception as e:
                response = f"Error: {str(e)}"

            print(f"!!!!!!!!!{response}")
            return render(request, 'home.html', {'form': form, 'server_response': response})
    else:
        form = HTTPRequestForm()

    return render(request, 'home.html', {'form': form, 'server_response': None})
