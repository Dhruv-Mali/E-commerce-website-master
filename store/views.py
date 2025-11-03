from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
import json
import datetime
import random
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

from .utils import cookieCart, product_sales_pipeline, send_order_confirmation_email
from .models import *


def store(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    products = Product.objects.all()
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if category:
        products = products.filter(category=category)
    
    categories = Product.objects.values_list('category', flat=True).distinct()

    context = {
        'products': products,
        'query': query,
        'categories': categories,
        'selected_category': category
    }
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
       
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        order = cookieData['order']
        items = cookieData['items']

    if request.POST.get('make-payment-btn') == 'make-payment-btn':
        try:
            if request.user.is_authenticated:
                customer, created = Customer.objects.get_or_create(user=request.user)
                order, created = Order.objects.get_or_create(customer=customer, complete=False)
                stripe_url = product_sales_pipeline(order.id, order.get_cart_total * 100)
            else:
                cookieData = cookieCart(request)
                order = cookieData['order']
                stripe_url = product_sales_pipeline(random.random(), order['get_cart_total'] * 100)
            
            if stripe_url:
                return HttpResponseRedirect(stripe_url)
            else:
                context = {'items': items, 'order': order, 'error': 'Payment gateway error'}
                return render(request, 'store/checkout.html', context)
        except Exception as e:
            context = {'items': items, 'order': order, 'error': str(e)}
            return render(request, 'store/checkout.html', context)
        
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)

def order_history(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/l/')
    
    customer, created = Customer.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(customer=customer, complete=True).order_by('-date_ordered')
    
    context = {'orders': orders}
    return render(request, 'store/order_history.html', context)

def cancelled(request):
    return render(request, 'store/cancelled.html')

def updateItem(request):
    if not request.user.is_authenticated:
        return JsonResponse("User not authenticated", safe=False)
    
    try:
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']

        customer, created = Customer.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            if product.stock > orderItem.quantity:
                orderItem.quantity = orderItem.quantity + 1
            else:
                return JsonResponse({"error": "Out of stock"}, safe=False)
        elif action == 'remove':
            orderItem.quantity = orderItem.quantity - 1

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse("Item updated", safe=False)
    except Exception as e:
        return JsonResponse(f"Error: {str(e)}", safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    
    else:

        name = data['form']['name']
        email = data['form']['email']

        cookieData = cookieCart(request)
        items = cookieData['items']

        customer, created = Customer.objects.get_or_create(
            email=email
        )
        customer.name = name
        customer.save()

        order = Order.objects.create(
            customer = customer,
            complete = False,
        )

        for item in items:
            product = Product.objects.get(id=item['product']['id'])

            orderItem = OrderItem.objects.create(
                product = product,
                order = order,
                quantity = item['quantity']
            )

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    
    # Update stock and send email
    for item in order.orderitem_set.all():
        product = item.product
        product.stock -= item.quantity
        product.save()
    
    # Send order confirmation email
    if customer.email:
        send_order_confirmation_email(customer.email, order)

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )


    return JsonResponse("Payment processed", safe=False)