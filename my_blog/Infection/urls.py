from django.urls import path

app_name = 'Infection'

from . import views

urlpatterns=[
    path('', views.processInfect, name='infection'),
]
