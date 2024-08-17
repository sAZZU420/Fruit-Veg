from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('shop/', views.shop, name='shop'),
    path('product_by_category/<slug:category_slug>', views.product_by_category, name='product_by_category'),
    path('product_by_price/', views.product_by_price, name='product_by_price'),

    path('shop_details/<slug:product_slug>', views.shop_details, name='shop_details'),

    path('search/', views.search, name='search'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_wishlist/<slug:product_slug>', views.add_wishlist, name='add_wishlist'),
    path('delete_wishlist/<slug:product_slug>', views.delete_wishlist, name='delete_wishlist'),

    path('rating_review/<slug:product_slug>', views.rating_review, name='rating_review'),

    path('product_by_color/', views.product_by_color, name='product_by_color'),
    path('product_by_size/', views.product_by_size, name='product_by_size'),

]
