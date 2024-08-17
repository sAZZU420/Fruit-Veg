from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("The Email must be set")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.is_admin = True

        user.save()
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=200)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = AccountManager()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    account_user = models.ForeignKey(Account, on_delete=models.CASCADE)

    user_profile_pic = models.ImageField(upload_to=f'profile_pic/{Account.username}', blank=True, null=True)
    user_cover_pic = models.ImageField(upload_to=f'cover_pic/{Account.username}', blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)

    last_login = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.account_user


class UserImages(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    user_images = models.ImageField(upload_to=f'user_images/{Account.username}', blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "userimages"
        verbose_name_plural = "user Images"

    def __unicode__(self):
        return self.user_profile
