import uuid
import random
import string
from django.conf import settings
from django.core.mail import send_mail
import json
from .models import Product, Customer, Order, OrderItem, ShippingAddress

# ─────────────────────────────────────────────
#  DEMO / MOCK Razorpay client (no real API keys needed)
# ─────────────────────────────────────────────
class _MockRazorpayClient:
    """Simulates the Razorpay SDK for college demo/educational projects."""
    pass

razorpay_client = _MockRazorpayClient()


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


def create_razorpay_order(amount_paise):
    """
    DEMO MODE: Simulates creating a Razorpay order.
    Returns a mock order dict without calling real API.
    """
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))
    mock_order = {
        'id': f'order_{random_suffix}',
        'amount': int(amount_paise),
        'currency': 'INR',
        'status': 'created',
    }
    return mock_order


def verify_razorpay_signature(payment_data):
    """
    DEMO MODE: Always returns True (no real signature check needed).
    """
    return True


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