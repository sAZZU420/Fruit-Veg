from .models import Category, WishList, Product, Variation


def categories(request):
    try:
        categories_for_all = Category.objects.all().order_by('-created_date')
    except Category.DoesNotExist:
        categories_for_all = None
    return dict(categories_for_all=categories_for_all)


def wishlists(request):
    total_wishlist = 0
    try:
        if request.user.is_authenticated:
            wishlists_for_all = WishList.objects.filter(user=request.user)
            total_wishlist = wishlists_for_all.count()
    except WishList.DoesNotExist:
        total_wishlist = 0
    return dict(total_wishlist=total_wishlist)


def wish_boxs(request):
    products = Product.objects.all()
    wish_box = []
    wish_box_user = []
    if request.user.is_authenticated:
        products = Product.objects.all()
        wish_box = []
        wish_box_user = []
        for product in products:
            try:
                wish_item = WishList.objects.get(user=request.user, product=product)
                wish_box.append(wish_item.product)
                wish_box_user.append(wish_item.user)
            except WishList.DoesNotExist:
                pass
    return dict(wish_box=wish_box)


def product_variation_color(request):
    variations = Variation.objects.filter(variation_category__iexact="color", is_active=True)
    total_color_variation = []
    for v in variations:
        if v.variation_value not in total_color_variation:
            total_color_variation.append(v.variation_value)
    return dict(total_color_variation=total_color_variation)


def product_variation_size(request):
    variations = Variation.objects.filter(variation_category__iexact="size", is_active=True)
    total_size_variation = []
    for v in variations:
        if v.variation_value not in total_size_variation:
            total_size_variation.append(v.variation_value)
    return dict(total_size_variation=total_size_variation)
