import stripe
from django.conf import settings
from django.core.mail import send_mail
import json
from .models import Product, Customer, Order, OrderItem, ShippingAddress

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
        stripe_price_obj = stripe.Price.create(
            product=stripe_product_obj.id,
            unit_amount=int(product_price),
            currency='inr'
        )
        
        base_endpoint = 'http://127.0.0.1:8000'
        checkout_session = stripe.checkout.Session.create(
            line_items=[{'price': stripe_price_obj.id, 'quantity': 1}],
            mode='payment',
            success_url=f"{base_endpoint}/payment-success/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{base_endpoint}/payment-cancelled/"
        )
        return checkout_session.url
    except stripe.error.AuthenticationError:
        raise Exception("Invalid Stripe API keys. Please check your keys at https://dashboard.stripe.com/test/apikeys")
    except Exception as e:
        raise Exception(f"Stripe error: {str(e)}")


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
        import sys
        sys.stderr.write(f"Email error: {str(e)}\n")