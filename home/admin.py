from django.contrib import admin
from .models import (
    Category,
    Product,
    Review,
    Slider,
    WishList,
    Variation
)


class ReviewAdminModel(admin.TabularInline):
    model = Review
    readonly_fields = ("user", "product", "product_image", "ratting", "review", "created_at")
    extra = 1


class ProductAdminModel(admin.TabularInline):
    model = Product
    readonly_fields = ("product_name", "product_slug", "product_image", "category", "description", "price", "in_stocks", "featured", "in_stock", "created_date")
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"category_slug": ('category_name',)}
    list_display = ("category_name", "featured", "created_date",)
    list_filter = ("category_name",)
    search_fields = ("category_name",)
    inlines = [ProductAdminModel]


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"product_slug": ('product_name',)}
    list_display = ("product_name", "category", "price", "in_stocks", "featured", "in_stock", "created_date")
    list_filter = ("product_name", "price", "featured", "in_stock",)
    search_fields = ("product_name",)
    inlines = [ReviewAdminModel]


class VariationAdmin(admin.ModelAdmin):
    list_display = ("product", "variation_category", "variation_value", "is_active", "create_at")
    list_filter = ("product", "variation_category", "variation_value",)
    search_fields = ("product", "variation_category", "variation_value",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "ratting", "created_at")
    list_filter = ("user", "product")
    search_fields = ("user", "product")
    ordering = ("-created_at",)


class WishListAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")
    list_filter = ("user", "product")
    search_fields = ("user", "product")
    ordering = ("-created_at",)


class SliderAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slider_slug": ('slider_name',)}
    list_display = ("slider_name", "created_date",)
    list_filter = ("slider_name",)
    search_fields = ("slider_name",)
    ordering = ("-created_date",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(Variation, VariationAdmin)
