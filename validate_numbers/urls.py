from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('validate/', views.process_phone_number, name='process_numbers'),
]