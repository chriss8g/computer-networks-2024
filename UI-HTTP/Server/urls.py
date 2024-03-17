from django.urls import path
from .views import ServerPageView

urlpatterns = [
    path('server/', ServerPageView, name='server'),
]