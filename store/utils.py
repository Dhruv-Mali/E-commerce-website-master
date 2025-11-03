import stripe
from django.conf import settings
from django.core.mail import send_mail
import json
from .models import *

stripe.api_key = settings.STRIPE_SECRET_KEY


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }

            items.append(item)
        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


def product_sales_pipeline(product_name, product_price):
    try:
        stripe_product_obj = stripe.Product.create(name=str(product_name))
        stripe_product_id = stripe_product_obj.id
        stripe_price_obj = stripe.Price.create(
            product=stripe_product_id,
            unit_amount=int(product_price),
            currency='inr'
        )
        
        # Use localhost for development
        base_endpoint = 'http://127.0.0.1:8000'
        success_url = f"{base_endpoint}/"
        cancel_url = f"{base_endpoint}/payments/cancelled/"

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': stripe_price_obj.id,
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url
        )
        return checkout_session.url
    except Exception as e:
        print(f"Stripe error: {e}")
        return None


def send_order_confirmation_email(email, order):
    try:
        subject = f'Order Confirmation - #{order.transaction_id}'
        message = f'''
Thank you for your order!

Order ID: {order.transaction_id}
Total Amount: ₹{order.get_cart_total}
Items: {order.get_cart_items}

Your order has been confirmed and will be processed shortly.

Thank you for shopping with us!
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Email error: {e}")