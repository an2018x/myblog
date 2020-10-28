from django.urls import path

app_name = 'Infection'

from . import views

urlpatterns=[
    path('chart', views.processInfect, name='infection'),
    path('list', views.processInfect2, name='infection2')
]
