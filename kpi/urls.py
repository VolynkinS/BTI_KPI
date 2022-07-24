from django.urls import path
from . import views

app_name = 'kpi'

urlpatterns = [
    path('fill/<int:pk>/', views.home, name='home'),
    path('answers/<int:pk>/', views.home_2, name='home_2'),
]
