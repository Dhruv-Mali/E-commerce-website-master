import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Order
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Handle payment success
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_successful_payment(session)
    
    # Handle payment failure
    elif event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']
        handle_failed_payment(session)
    
    return HttpResponse(status=200)

def handle_successful_payment(session):
    """Process successful payment"""
    payment_intent = session.get('payment_intent')
    try:
        order = Order.objects.get(stripe_payment_intent=payment_intent)
        order.complete = True
        order.status = 'processing'
        order.save()
        
        # Reduce stock
        for item in order.orderitem_set.all():
            if item.product:
                item.product.reduce_stock(item.quantity)
    except Order.DoesNotExist:
        pass

def handle_failed_payment(session):
    """Handle failed payment"""
    payment_intent = session.get('payment_intent')
    try:
        order = Order.objects.get(stripe_payment_intent=payment_intent)
        order.status = 'cancelled'
        order.save()
    except Order.DoesNotExist:
        pass
