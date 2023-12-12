from django.urls import path
from . import views

urlpatterns = [
    path('invocations', views.invocations, name='invocations'),
    path('ping', views.health_check, name='health_check'),
    path('', views.health_check, name='health_check'),
]