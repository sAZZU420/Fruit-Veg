from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem, Cart
from order.models import Order, OrderProduct, Payment
import uuid
from django.contrib import messages

from sslcommerz_lib import SSLCOMMERZ
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site

from django.conf import settings


@login_required(login_url='/account/')
def checkout(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            value1 = request.POST.get("subtotal")
            value1_split = value1.split(',', 1)
            subtotal_value = "".join(value1_split)
            subtotal = float(subtotal_value)

            value2= request.POST.get("tax")
            value2_split = value2.split(',', 1)
            tax_value = "".join(value2_split)
            tax = float(tax_value)

            value3 = request.POST.get("total")
            value3_split = value3.split(',', 1)
            total_value = "".join(value3_split)
            total = float(total_value)

            cart_items = CartItem.objects.filter(user=request.user)
            context = {
                'cart_items': cart_items,
                'subtotal': subtotal,
                'tax': tax,
                'total': total,
            }
        return render(request, 'order/checkout.html', context)


@login_required(login_url='/account/')
def billing_details(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            address = request.POST.get('address')
            address2 = request.POST.get('address2')
            city = request.POST.get('city')
            country = request.POST.get('country')
            state = request.POST.get('state')
            zip_code = request.POST.get('zip_code')

            total_order_make = request.POST.get('total_value_for_order')
            value1 = total_order_make.split(',', 1)
            value1_join = "".join(value1)
            total_order = float(value1_join)

            tax_value_make = request.POST.get('tax_value_for_order')
            value2 = tax_value_make.split(',', 1)
            value2_join = "".join(value2)
            tax = float(value2_join)

            order_number = uuid.uuid4().hex[:15]

            create_order = Order.objects.create(
                user=request.user,
                order_number=order_number,
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile=mobile,
                address=address,
                address2=address2,
                city=city,
                country=country,
                state=state,
                zip_code=zip_code,
                total_order=total_order,
                tax=tax,
                ip=request.META['REMOTE_ADDR']
            )
            create_order.save()
            messages.success(request, 'checkout')
            return redirect('payment_details', order_number=order_number)
        #     order create done
        #     create payment
        return render(request, 'order/checkout.html')


def payment_details(request, order_number):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        order = Order.objects.get(user=request.user, order_number=order_number)
        total = order.total_order
        tax = order.tax
        subtotal = (total-tax)
        context = {
            'cart_items': cart_items,
            'order': order,
            'total': total,
            'tax': tax,
            'subtotal': subtotal,
        }
        return render(request, 'order/payment_details.html', context)
    return render(request, 'order/payment_details.html')


def payment_method(request, order_number):
    if request.user.is_authenticated:
        if request.method == "POST":
            input_value = request.POST.get('payment')
            if input_value == "cash":
                order = Order.objects.get(is_ordered=False, order_number=order_number)

                payment = Payment.objects.create(
                    user=request.user,
                    payment_id=order_number,
                    payment_method="cash ON Delivery",
                    amount_paid="0",
                    status="DUE",
                )
                payment.save()

                order.payment = payment
                order.is_ordered = True
                order.status = payment.status
                order.save()
                messages.success(request, 'Cash ON Delivery')
                return redirect('payment_successful', order_number=order_number)

            elif input_value == "sslcommerz":
                order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)

                store_id = settings.STORE_ID
                store_password = settings.STORE_PASSWORD
                ssl_cz = SSLCOMMERZ({'store_id': store_id, 'store_pass': store_password, 'issandbox': True})
                current_webpage = get_current_site(request).domain
                url = f'http://{current_webpage}/sslcommerz_successful/'
                data = {
                    'total_amount': order.total_order,
                    'currency': "BDT",
                    'tran_id': order.order_number,
                    'success_url': url,
                    # if transaction is successful, user will be redirected here
                    'fail_url': url,
                    # if transaction is failed, user will be redirected here
                    'cancel_url': url,
                    # after user cancels the transaction, will be redirected here
                    'emi_option': "0",
                    'cus_name': order.full_name,
                    'cus_email': order.email,
                    'cus_phone': order.mobile,
                    'cus_add1': order.address,
                    'cus_city': order.city,
                    'cus_country': order.country,
                    'shipping_method': "NO",
                    'multi_card_name': "",
                    'num_of_item': 1,
                    'product_name': "Test",
                    'product_category': "Test Category",
                    'product_profile': "general",
                }
                response = ssl_cz.createSession(data)
                return redirect(response['GatewayPageURL'])
            else:
                return render(request, 'order/payment_details.html')
        return render(request, 'order/payment_details.html')
    return render(request, 'order/payment_details.html')


@csrf_exempt
def sslcommerz_successful(request):
    if request.method == "POST":
        response = request.POST
        order_number = response['tran_id']
        payment_number = response['val_id']
        payment_system = response['card_issuer']
        total_paid = response['amount']
        status = response['status']
        date_time = response['tran_date']
        order = Order.objects.get(is_ordered=False, order_number=order_number)

        payment = Payment.objects.create(
            user=order.user,
            payment_id=payment_number,
            payment_method=payment_system,
            amount_paid=total_paid,
            status=status,
            created_at=date_time
            )
        payment.save()

        order = Order.objects.get(is_ordered=False, order_number=order_number)
        order.payment = payment
        order.is_ordered = True
        order.status = payment.status
        order.save()
        return redirect("payment_successful", order_number=order_number)


@csrf_exempt
def sslcommerz_fail(request):
    return redirect("payment_successful")


@csrf_exempt
def sslcommerz_cancel(request):
    return redirect("payment_successful")


def payment_successful(request, order_number):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        order = Order.objects.get(user=request.user, order_number=order_number)
        total = order.total_order
        tax = order.tax
        subtotal = (total - tax)
        context = {
            'cart_items': cart_items,
            'order': order,
            'total': total,
            'tax': tax,
            'subtotal': subtotal,
        }
        return render(request, 'order/payment_successful.html', context)