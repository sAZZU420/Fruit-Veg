from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.cart, name='cart'),

    path('add_cart/<slug:product_slug>', views.add_cart, name='add_cart'),
    path('remove_cart/<slug:product_slug>/<int:cart_id>/', views.remove_cart, name='remove_cart'),
    path('delete_cart/<slug:product_slug>/<int:cart_id>/', views.delete_cart, name='delete_cart'),

]

