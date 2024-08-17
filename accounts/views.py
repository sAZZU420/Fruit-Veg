from django.shortcuts import render, redirect
import uuid
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from cart.models import Cart, CartItem
from cart.views import _cart_id
from home.models import Product

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q


def registration(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("reg-email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("reg-password")
        confirm_password = request.POST.get("reg-confirm_password")
        try:
            match_user = Account.objects.get(email=email)
            messages.error(request, 'email used!!!!')
            return redirect('account')
        except (Account.DoesNotExist, ValueError, OverflowError, TypeError):
            if password != confirm_password:
                messages.error(request, 'pass not match!!!!')
                return redirect('account')
            else:
                new_user = Account.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=email.split('@', 1)[0],
                    )
                new_user.phone_number = mobile
                new_user.set_password(password)
                new_user.save()

                new_user = Account.objects.get(email=email)
                domain = get_current_site(request)
                mail_sub = "Please Click the link to activate Your Account"
                message = render_to_string('accounts/account_verification.html', {
                    'user': new_user,
                    'domain': domain,
                    'email': new_user.email,
                    'uuid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': default_token_generator.make_token(new_user),
                })
                plain_message = strip_tags(message)
                send_email = EmailMultiAlternatives(subject=mail_sub, body=plain_message, to=[email])
                send_email.attach_alternative(message, "text/html")
                send_email.send()

                messages.success(request, 'success')
                context = {
                    'user': new_user,
                }
                return render(request, 'accounts/registration.html', context)
    else:
        return render(request, 'accounts/registration.html')


def registration_success(request, email, token, uuid):
    try:
        uid = urlsafe_base64_decode(uuid).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account Activate')
        return redirect('account')
    else:
        messages.error(request, 'Activation fail')
        return redirect('registration')


def login_user(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')
        account = Account.objects.get(email=email)
        match = account.check_password(password)
        if match:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                try:
                    try:
                        cart = Cart.objects.get(cart_id=_cart_id(request))
                    except Cart.DoesNotExist:
                        cart = Cart.objects.create(cart_id=_cart_id(request))
                    cart_items = CartItem.objects.filter(cart=cart)
                    cart_items_variation = []
                    cart_items_id = []
                    for v in cart_items:
                        variations = v.variation.all()
                        product_name = Product.objects.filter(product_slug=v.product.product_slug)
                        list_variation = list(variations)
                        product_name_list = list(product_name)
                        list_variation.append(product_name_list[0])
                        cart_items_variation.append(list_variation)
                        cart_items_id.append(v.id)

                    cart_items_by_user = CartItem.objects.filter(user=user)
                    user_cart_items_variation = []
                    user_cart_items_id = []
                    for u in cart_items_by_user:
                        variation = u.variation.all()
                        product_user = Product.objects.filter(product_slug=u.product.product_slug)
                        variation_list = list(variation)
                        product_list = list(product_user)
                        variation_list.append(product_list[0])
                        user_cart_items_variation.append(variation_list)
                        user_cart_items_id.append(u.id)
                    for cart in cart_items_variation:
                        if cart in user_cart_items_variation:
                            index_cart = cart_items_variation.index(cart)
                            item_id_cart = cart_items_id[index_cart]
                            item_cart = CartItem.objects.get(id=item_id_cart)

                            index_user = user_cart_items_variation.index(cart)
                            item_id = user_cart_items_id[index_user]
                            item_user = CartItem.objects.get(id=item_id)
                            item_user.quantity += item_cart.quantity
                            item_user.save()

                        else:
                            index_cart = cart_items_variation.index(cart)
                            item_id_cart = cart_items_id[index_cart]
                            item_cart = CartItem.objects.get(id=item_id_cart)
                            item_cart.user = user
                            item_cart.save()
                except (ValueError, OverflowError, TypeError):
                    pass
                login(request, user)
                messages.success(request, "welcome...")
                if '/?next=' in request.META.get('HTTP_REFERER'):
                    get_url = request.META.get('HTTP_REFERER')
                    step1 = get_url.split("/account/?next=",)
                    step2 = step1[1]
                    url = "".join(step1)
                    return redirect(url)
                else:
                    return redirect('dashboard')
        else:
            messages.error(request,  "wrong pass!!!")
            return redirect('account')
    else:
        return render(request, 'accounts/login.html')


def forget_password(request):
    if request.method == "GET":
        email = request.GET.get('forget_email')
        try:
            account_found = Account.objects.get(email=email)
            if account_found:
                token_generate = uuid.uuid4().hex[:5]
                token_encode = urlsafe_base64_encode(force_bytes(token_generate))
                mail_sub = "Reset Password Code"
                message = render_to_string('accounts/reset_pass_code_email.html', {
                    'token': token_generate,
                })
                plain_message = strip_tags(message)
                send_email = EmailMultiAlternatives(subject=mail_sub, body=plain_message, to=[email])
                send_email.attach_alternative(message, "text/html")
                send_email.send()
                messages.success(request, 'Email Send...')
                return redirect('confirm_token', token_generate=token_encode, email=email)
            else:
                messages.error(request, 'Not Found!!!')
                return redirect('account')
        except Account.DoesNotExist:
            messages.error(request, 'Not Found!!!')
            return redirect('account')

    return render(request, 'accounts/forget_password.html')


def confirm_token(request, token_generate, email):
    if request.method == "POST":
        get_token = request.POST.get('email_token')
        token_decode = urlsafe_base64_decode(token_generate).decode()
        if token_decode == get_token:
            messages.success(request, 'code match...')
            return redirect('reset_password', email=email)
        else:
            messages.error(request, 'Wrong Code!!!')
            return render(request, 'accounts/confirm_token.html')
    return render(request, 'accounts/confirm_token.html')


def reset_password(request, email):
    try:
        user_found = Account.objects.get(email=email)
    except:
        user_found = None
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password == confirm_password:
            user = Account.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'pass changed...')
            return redirect("account")
        else:
            messages.error(request, 'pass not match!!!')
            return render(request, 'accounts/forget_password.html')
    return render(request, 'accounts/forget_password.html')


@login_required(login_url='/account/')
def logout_user(request):
    try:
        logout(request)
        messages.success(request, 'Logout...')
    except:
        pass
    return redirect('account')


@login_required(login_url='/account/')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
