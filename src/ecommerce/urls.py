from django.urls import path
from . import views

app_name = 'ecommerce'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
]
