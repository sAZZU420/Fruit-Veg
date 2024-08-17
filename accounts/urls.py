from django.urls import path
from . import views
import uuid


token_generate1 = uuid.uuid4().hex[:8]
token_generate2 = uuid.uuid4().hex[:12]
urlpatterns = [
        path("account/", views.login_user, name="account"),
        path("dashboard/", views.dashboard, name="dashboard"),

        path("logout/", views.logout_user, name="logout"),

        path("registration/", views.registration, name="registration"),
        path("registration/<email>/<token>/<uuid>", views.registration_success, name="registration_success"),

        path("forget_password/", views.forget_password, name="forget_password"),
        path(f"confirm_token/<email>/{token_generate1}<token_generate>{token_generate2}/", views.confirm_token, name="confirm_token"),
        path("reset_password/<email>/", views.reset_password, name="reset_password"),
]
