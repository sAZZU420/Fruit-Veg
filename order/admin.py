from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'payment', 'order', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'order_number', 'payment', 'is_ordered', 'status', 'total_order', 'mobile', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'payment', 'email', 'phone', 'is_ordered']
    list_per_page = 20
    inlines = [OrderProductInline]

    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment', 'order', 'product', 'quantity', 'product_price', 'ordered')
    list_filter = ('user', 'payment', 'order', 'product',)
    search_fields = ('user', 'payment', 'order', 'product',)
    list_per_page = 20


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_id', 'payment_method', 'amount_paid', 'status', 'created_at']
    list_filter = ['user', 'payment_id', 'payment_method']
    search_fields = ['user', 'payment_id', 'payment_method']
    list_per_page = 20


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
