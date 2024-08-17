from .models import Cart, CartItem
from .views import _cart_id


def cart_count(request):
    cart_items = []
    if request.user.is_authenticated:
        try:
            cart_items = CartItem.objects.filter(user=request.user)
        except (CartItem.DoesNotExist, ValueError, OverflowError):
            cart_items = 0
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        try:
            cart_items = CartItem.objects.filter(cart=cart)
        except (CartItem.DoesNotExist, ValueError, OverflowError):
            cart_items = None
    cart_total = cart_items.count()
    return dict(cart_total=cart_total)
