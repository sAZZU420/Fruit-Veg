from django.db import models
from accounts.models import Account
from django.db.models import Avg


class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    category_slug = models.SlugField(max_length=200, unique=True)
    category_image = models.ImageField(upload_to='category_images', blank=True, null=True)

    featured = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']
        verbose_name = "category"
        verbose_name_plural = "categories"

    def total_products(self):
        products = Product.objects.filter(category__category_name=self.category_name)
        total_product = products.count()
        return total_product

    def __str__(self):
        return self.category_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    product_name = models.CharField(max_length=200, unique=True)
    product_slug = models.SlugField(max_length=200, unique=True)
    product_image = models.ImageField(upload_to='product_images')
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField(null=True, blank=True, default='N/A')
    in_stocks = models.IntegerField()

    featured = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def product_average_review(self):
        total = 0
        reviews = Review.objects.filter(product__product_slug=self.product_slug).aggregate(Avg("ratting", default=0))
        review = reviews['ratting__avg']
        return review

    def product_review_count(self, total=0):
        reviews = Review.objects.filter(product__product_name=self.product_name)
        total_reviews = reviews.count()
        return total_reviews

    def __str__(self):
        return self.product_name


class Slider(models.Model):
    slider_name = models.CharField(max_length=200)
    slider_slug = models.SlugField(max_length=200)
    banner = models.ImageField(upload_to='slider_images')
    show = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slider_name


class Review(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    product_image = models.ImageField(upload_to='review_images', blank=True, null=True)
    review = models.TextField(max_length=1000)
    ratting = models.FloatField()
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user


class WishList(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category="color", is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category="size", is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    variation_category = models.CharField(max_length=100, choices=variation_category_choice, default=None)
    variation_value = models.CharField(max_length=100, default=None)

    is_active = models.BooleanField(default=True)

    create_at = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
