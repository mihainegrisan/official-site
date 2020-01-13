from django.urls import path
from . import views

app_name = 'cv'

urlpatterns = [
    path('home1/', views.home_1, name='home_1'),
    path('home2/', views.home_2, name='home_2'),
]
