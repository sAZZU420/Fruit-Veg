from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("billing details/", views.billing_details, name="billing_details"),

    path("payment details/<order_number>", views.payment_details, name="payment_details"),
    path("payment method/<order_number>", views.payment_method, name="payment_method"),

    path("sslcommerz_successful/", views.sslcommerz_successful, name="sslcommerz_successful"),
    path("sslcommerz_fail/", views.sslcommerz_fail, name="sslcommerz_fail"),
    path("sslcommerz_cancel/", views.sslcommerz_cancel, name="sslcommerz_cancel"),

    path("payment successful/<order_number>", views.payment_successful, name="payment_successful"),
]
