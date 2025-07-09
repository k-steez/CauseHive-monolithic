from .views import (add_to_cart, update_cart_item, checkout, get_cart, remove_from_cart)
from django.urls import path

urlpatterns = [
    path('', get_cart, name='get_cart'),
    path('add/', add_to_cart, name='add_to_cart'),
    path('donations/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('donations/<int:item_id>/remove/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
]