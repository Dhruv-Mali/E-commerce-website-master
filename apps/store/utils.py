import razorpay
from django.conf import settings
from django.core.mail import send_mail
import json
from .models import Product, Customer, Order, OrderItem, ShippingAddress

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


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
    Create a Razorpay order.
    amount_paise: amount in paise (e.g. ₹100 = 10000 paise)
    Returns the Razorpay order dict or raises an exception.
    """
    try:
        order_data = {
            'amount': int(amount_paise),
            'currency': 'INR',
            'payment_capture': 1  # auto-capture after payment
        }
        razorpay_order = razorpay_client.order.create(data=order_data)
        return razorpay_order
    except razorpay.errors.BadRequestError as e:
        raise Exception(f"Razorpay error: {str(e)}")
    except Exception as e:
        raise Exception(f"Razorpay error: {str(e)}")


def verify_razorpay_signature(payment_data):
    """
    Verify Razorpay payment signature.
    payment_data must contain: razorpay_order_id, razorpay_payment_id, razorpay_signature
    Returns True if valid, raises SignatureVerificationError otherwise.
    """
    razorpay_client.utility.verify_payment_signature(payment_data)
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