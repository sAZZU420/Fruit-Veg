from django.shortcuts import render, redirect
from .models import Product, WishList, Review, Variation
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import datetime


def home(request):
    recent_products = None
    featured_products = None
    try:
        featured = Product.objects.filter(featured=True)
        pagination = Paginator(featured, '11')
        pages = request.GET.get("page")
        featured_products = pagination.get_page(pages)
    except:
        pass
    try:
        recent = Product.objects.all().order_by('-created_date')
        pagination = Paginator(recent, '11')
        pages = request.GET.get("page")
        recent_products = pagination.get_page(pages)
    except:
        pass
    context = {
        'recent_products': recent_products,
        'featured_products': featured_products
    }
    return render(request, 'home/home.html', context)


def shop(request):
    try:
        pro = Product.objects.all()
        page_number = request.GET.get("page")
        paginator = Paginator(pro, 20)
        products = paginator.get_page(page_number)
        tuples = products.paginator.num_pages
        total_page = []
        for p in range(0, tuples):
            num = p+1
            total_page.append(num)
        total = pro.count()
        context = {
            'products': products,
            'total': total,
            'total_page': total_page,
        }
        return render(request, 'home/shop.html', context)
    except:
        return render(request, 'home/shop.html')


def product_by_category(request, category_slug):
    try:
        pro = Product.objects.filter(category__category_slug=category_slug)
        total = pro.count()
        paginator = Paginator(pro, 20)
        page_number = request.GET.get("page")
        products = paginator.get_page(page_number)
        tuples = products.paginator.num_pages
        total_page = []
        for p in range(0, tuples):
            num = p + 1
            total_page.append(num)
        total = pro.count()
        context = {

            'products': products,
            'total': total,
            'total_page': total_page,
        }
        return render(request, 'home/shop.html', context)
    except:
        return render(request, 'home/shop.html')


def product_by_price(request):
    if request.method == "GET":
        value = request.GET.get('price')
        if int(value) < 500:
            pro = Product.objects.filter(price__in=range(0, 500))
        elif int(value) >= 500 and int(value) < 1000:
            pro = Product.objects.filter(price__in=range(500, 1000))
        elif int(value) >= 1000 and int(value) < 2000:
            pro = Product.objects.filter(price__in=range(1000, 2000))
        elif int(value) >= 2000 and int(value) < 4000:
            pro = Product.objects.filter(price__in=range(2000, 4000))
        elif int(value) >= 4000:
            pro = Product.objects.all()
        else:
            pro = Product.objects.all()
    else:
        value = 0
        pro = 0
    prod = []
    for p in pro:
        prod.append(p)
    paginator = Paginator(prod, 20)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)
    tuples = products.paginator.num_pages
    total_page = []
    for p in range(0, tuples):
        num = p + 1
        total_page.append(num)
    total = pro.count()
    context = {
        'products': products,
        'total': total,
        'total_page': total_page,
    }
    return render(request, 'home/shop.html', context)


def product_by_color(request):
    if request.method == "GET":
        category = "color"
        value = request.GET.get('color')
        products = []
        variation = Variation.objects.filter(variation_category__iexact=category, variation_value__iexact=value)
        for p in variation:
            products.append(p.product)
    else:
        products = 0
        variation = 0
    prod = []
    for p in products:
        prod.append(p)
    paginator = Paginator(prod, 20)
    page_number = request.GET.get("page")
    product = paginator.get_page(page_number)
    tuples = product.paginator.num_pages
    total_page = []
    for p in range(0, tuples):
        num = p + 1
        total_page.append(num)
    total = variation.count()
    context = {
        'products': products,
        'total': total,
        'total_page': total_page,
        # 'value_is': int(value)
    }
    return render(request, 'home/shop.html', context)


def product_by_size(request):
    if request.method == "GET":
        category = "size"
        value = request.GET.get('size')
        products = []
        variation = Variation.objects.filter(variation_category__iexact=category, variation_value__iexact=value)
        for p in variation:
            products.append(p.product)
    else:
        products = 0
        variation = 0
    prod = []
    for p in products:
        prod.append(p)
    paginator = Paginator(prod, 20)
    page_number = request.GET.get("page")
    product = paginator.get_page(page_number)
    tuples = product.paginator.num_pages
    total_page = []
    for p in range(0, tuples):
        num = p + 1
        total_page.append(num)
    total = variation.count()
    context = {
        'products': products,
        'total': total,
        'total_page': total_page,
        # 'value_is': int(value)
    }
    return render(request, 'home/shop.html', context)


def shop_details(request, product_slug):
    single_product = Product.objects.get(product_slug=product_slug)
    related_products = Product.objects.filter(category=single_product.category)

    variation = Variation.objects.filter(product__product_slug=product_slug)
    variation_colors = []
    variation_sizes = []
    for v in variation:
        if v.variation_category == "color":
            variation_colors.append(v.variation_value)
        if v.variation_category == "size":
            variation_sizes.append(v.variation_value)
        else:
            pass

    reps = Review.objects.filter(product__product_slug=product_slug)
    re = []
    for r in reps:
        re.append(r)
    pagination = Paginator(re, '3')
    pages = request.GET.get("page")
    reviews_ratings = pagination.get_page(pages)

    tuples = reviews_ratings.paginator.num_pages
    total_page = []
    for p in range(0, tuples):
        num = p + 1
        total_page.append(num)

    context = {
        'single_product': single_product,
        'related_products': related_products,
        'reviews_ratings': reviews_ratings,
        'total_page': total_page,
        'variation_colors': variation_colors,
        'variation_sizes': variation_sizes
    }
    return render(request, 'home/shop_details.html', context)


def search(request):
    if request.method == "GET":
        search_value = request.GET.get('search_product')

        pro = Product.objects.filter(Q(product_slug__icontains=search_value) | Q(description__icontains=search_value) | Q(category__category_slug__icontains=search_value))
        if pro:
            total = pro.count()
            paginator = Paginator(pro, 20)
            page_number = request.GET.get("page")
            products = paginator.get_page(page_number)

            tuples = products.paginator.num_pages
            total_pages = []
            for p in range(0, tuples):
                num = p + 1
                total_pages.append(num)
            print('total-----------------------', total)
            context = {
                "products": products,
                "total": total,
                'total_page': total_pages,
                'search_value': search_value
            }
        else:
            total = 0
            context = {
                "total": total,
            }
            return render(request, 'home/shop.html', context)


@login_required(login_url='/account/')
def wishlist(request):
    if request.user.is_authenticated:
        wishes = None
        wishlists = []
        try:
            wishes = WishList.objects.filter(user=request.user)
            for wish in wishes:
                wishlists.append(wish.product)
        except:
            pass

        total = wishes.count()
        paginator = Paginator(wishlists, 20)
        page_number = request.GET.get("page")
        products = paginator.get_page(page_number)
        context = {
            'products': products,
            'total': total,
        }
        return render(request, 'home/shop.html', context)
    return render(request, 'home/shop.html')


@login_required(login_url='/account/')
def add_wishlist(request, product_slug):
    if request.user.is_authenticated:
        try:
            wishlist = WishList.objects.get(user=request.user, product__product_slug=product_slug)
        except:
            product = Product.objects.get(product_slug=product_slug)
            create_wishlist = WishList.objects.create(
                user=request.user,
                product=product
            )
            create_wishlist.save()
        get_url = request.META['HTTP_REFERER']
        if "?next=" in get_url:
            return redirect('wishlist')
        else:
            return redirect(get_url)


@login_required(login_url='/account/')
def delete_wishlist(request, product_slug):
    if request.user.is_authenticated:
        try:
            get_wishlist = WishList.objects.get(user=request.user, product__product_slug=product_slug)
            get_wishlist.delete()
        except (WishList.DoesNotExist, ValueError):
            pass
        url = request.META['HTTP_REFERER']
        return redirect(url)


@login_required(login_url='/account/')
def rating_review(request, product_slug):
    if request.user.is_authenticated:
        if request.method == "POST":
            rating_get = request.POST.get('rating')
            review_get = request.POST.get('review')
            product = Product.objects.get(product_slug=product_slug)
            user = request.user
            try:
                reviews = Review.objects.get(user=user, product=product)
                reviews.ratting = rating_get
                reviews.review = review_get
                reviews.created_at = datetime.datetime.now()
                reviews.save()
            except Review.DoesNotExist:
                reviews = Review.objects.create(
                    user=user,
                    product=product,
                    product_image=product.product_image,
                    review=review_get,
                    ratting=rating_get,
                )
                reviews.save()
            return redirect('shop_details', product_slug=product_slug)
