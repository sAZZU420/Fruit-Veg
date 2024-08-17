from django.contrib import admin
from .models import Account, UserProfile, UserImages
from django.contrib.auth.admin import UserAdmin


class AccountManager(admin.ModelAdmin):
    list_display = ("email", "is_admin", "is_superuser", "is_staff", "is_active", "last_login", "date_joined")
    list_editable = ("is_admin", "is_superuser", "is_staff", "is_active")
    list_filter = ("email", "is_admin", "is_superuser", "is_staff", "is_active", "last_login")
    filter_horizontal = ()
    search_fields = ("email",)
    ordering = ('-date_joined',)


class UserImagesManager(admin.TabularInline):
    model = UserImages
    extra = 1


class UserProfileManager(admin.ModelAdmin):
    list_display = ("account_user", "address", "city", "country", "last_login",)
    list_filter = ("account_user",)
    search_fields = ("account_user",)
    inlines = [UserImagesManager]


admin.site.register(Account, AccountManager)
admin.site.register(UserProfile, UserProfileManager)
admin.site.register(UserImages)
