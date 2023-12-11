import datetime
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from cart.models import CartItem
from users.models import CustomUser
from django.utils import timezone
from products.models import Product
from .models import Order, OrderProduct, Payment
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .form import OrderForm
from django.contrib import messages
# Create your views here.


def payment(request):
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body["orderID"])

    # STORE TRANSACTION DETAILS INSIDE PAYMENT MODEL
    payment = Payment(
        user=request.user,
        payment_id=body["transID"],
        payment_method=body["payment_method"],
        amount_paid=order.order_total,
        status=body["status"]
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # MOVE THE CARTS ITEMS TO ORDER PRODUCT TABLE
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        order_product = OrderProduct()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id = request.user.id
        order_product.product_id = item.product_id
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # IF THE CART COUNT IS LESS THAN OR EQUAL TO 0, THEN REDIRECT BACK TO HOME OR ALL PRODUCTS
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("home")

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # STORE ALL THE BILLING INFORMATION INSIDE ORDER TABLE
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.email = form.cleaned_data["email"]
            data.phone_number = form.cleaned_data["phone_number"]
            data.city = form.cleaned_data["city"]
            data.address_line = form.cleaned_data["address_line"]
            data.departament = form.cleaned_data["departament"]
            data.number_dui = form.cleaned_data["number_dui"]
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()

            # GENERATE ORDER NUMBER
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)

            return render(request, "payment.html", {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            })
        else:
            for error in list(form.errors.values()).pop():
                messages.error(request, error)
            return redirect("checkout")
    else:
        return redirect("checkout")


def order_complete(request):
    order_number = request.GET.get("order_number")
    transID = request.GET.get("payment_id")

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0

        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        return render(request, 'order_complete.html', {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        })
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
