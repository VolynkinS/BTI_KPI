from django.urls import path
from . import views

app_name = 'kpi'

urlpatterns = [
    # path('', views.home, name='home'),
    path('<int:pk>/', views.home_new_1, name='home_new_1'),
    path('answers/<int:pk>/', views.home_2, name='home_2'),

]
