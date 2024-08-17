from django.db import models
from home.models import Product, Variation
from accounts.models import Account


class Cart(models.Model):
    cart_id = models.CharField(max_length=200)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)

    quantity = models.IntegerField()

    in_available = models.BooleanField(default=True)

    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_add']

    def get_total(self):
        return self.quantity * self.product.price

    def __unicode__(self):
        return self.product


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=100, unique=True)
    discount = models.PositiveIntegerField(help_text='discount in percentage')
    active = models.BooleanField(default=True)
    active_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    required_amount_to_use_coupon = models.PositiveIntegerField()
    limit_to_use_coupon = models.PositiveIntegerField(default=100, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.coupon_code
