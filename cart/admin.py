from django.contrib import admin
from .models import Cart, CartItem, Coupon


class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "added_date")
    list_filter = ("cart_id", "added_date")
    search_fields = ("cart_id",)
    ordering = ("-added_date",)
    list_per_page = 20


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "cart", "quantity", "in_available", "date_add")
    list_filter = ("user", "product")
    search_fields = ("user", "product")
    list_per_page = 20


class CouponAdmin(admin.ModelAdmin):
    list_display = ("coupon_code", "discount", "active_date", "expiry_date", "required_amount_to_use_coupon", "limit_to_use_coupon", "create_date")
    list_filter = ("coupon_code", "active_date", "expiry_date",)
    search_fields = ("coupon_code",)
    list_per_page = 20


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Coupon, CouponAdmin)
