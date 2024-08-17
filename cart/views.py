from django.shortcuts import render, redirect
from home.models import Product, Variation
from .models import Cart, CartItem, Coupon
from django.db.models import Q


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_slug):
    quantities = request.POST.get('quantity')
    if quantities is None:
        value = 1
    else:
        value = int(quantities)

    product = Product.objects.get(product_slug=product_slug)
    product_variations = []
    # variation
    if request.method == "POST":
        for item in request.POST:
            key = item
            values = request.POST[key]
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=values)
                product_variations.append(variation)
            except Variation.DoesNotExist:
                pass
    # if user active
    if request.user.is_authenticated:
        try:
            cart_variations = []
            cart_id = []
            cart_items = CartItem.objects.filter(user=request.user, product=product)
            for c in cart_items:
                car = c.variation.all()
                cart_variations.append(list(car))
                cart_id.append(c.id)
            if product_variations in cart_variations:
                index = cart_variations.index(product_variations)
                item_id = cart_id[index]
                cart_item = CartItem.objects.get(product=product, id=item_id)
                cart_item.quantity += value
                cart_item.save()

            else:
                cart_item = CartItem.objects.create(
                    user=request.user,
                    product=product,
                    quantity=value
                )
                if len(product_variations) > 0:
                    cart_item.variation.clear()
                    for v in product_variations:
                        cart_item.variation.add(v)
                cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                user=request.user,
                product=product,
                quantity=value
            )
            if len(product_variations) > 0:
                cart_item.variation.clear()
                for v in product_variations:
                    cart_item.variation.add(v)

            cart_item.save()
    else:
        try:
            carts = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist():
            carts = Cart.objects.create(cart_id=_cart_id(request))
        try:
            cart_variations = []
            cart_id = []
            cart_items = CartItem.objects.filter(cart=carts, product=product)
            for c in cart_items:
                car = c.variation.all()
                cart_variations.append(list(car))
                cart_id.append(c.id)
            if product_variations in cart_variations:
                index = cart_variations.index(product_variations)
                item_id = cart_id[index]
                cart_item = CartItem.objects.get(product=product, id=item_id)
                cart_item.quantity += value
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    cart=carts,
                    product=product,
                    quantity=value
                )
                if len(product_variations) > 0:
                    cart_item.variation.clear()
                    for v in product_variations:
                        cart_item.variation.add(v)
                cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart=carts,
                product=product,
                quantity=value
            )
            if len(product_variations) > 0:
                cart_item.variation.clear()
                for v in product_variations:
                    cart_item.variation.add(v)

            cart_item.save()
    return redirect('cart')


def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))
    subtotal = 0
    for cart_item in cart_items:
        subtotal += cart_item.product.price * cart_item.quantity

    if request.method == "GET":
        coupon_code = request.GET.get('coupon')
        try:
            coupon = Coupon.objects.get(coupon_code__iexact=coupon_code)
            if subtotal > coupon.required_amount_to_use_coupon:
                discount_value = float(subtotal) * (coupon.discount/100)
            else:
                discount_value = 0
            total_amount = subtotal - int(discount_value)
        except Coupon.DoesNotExist:
            total_amount = subtotal
            coupon = None
    else:
        total_amount = subtotal
        coupon = None
    tax = int(total_amount) * 0.15
    total = int(total_amount)+tax
    context = {
        "cart_items": cart_items,
        'subtotal': total_amount,
        'tax': tax,
        'total': total,
        'coupon': coupon
    }
    return render(request, 'cart/cart.html', context)


def remove_cart(request, product_slug, cart_id):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(user=request.user, product__product_slug=product_slug, id=cart_id)
    else:
        cart_item = CartItem.objects.get(cart__cart_id=_cart_id(request), product__product_slug=product_slug, id=cart_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def delete_cart(request, product_slug, cart_id):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(user=request.user, product__product_slug=product_slug, id=cart_id)
    else:
        cart_item = CartItem.objects.get(cart__cart_id=_cart_id(request), product__product_slug=product_slug, id=cart_id)
    cart_item.delete()
    return redirect('cart')
