from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.db import transaction
from django.core.exceptions import ValidationError
import json
import datetime
import random
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

from .utils import cookieCart, product_sales_pipeline, send_order_confirmation_email
from .models import *

# Import validators with fallback
try:
    from .validators import validate_order_total, validate_stock_availability, sanitize_search_query
except ImportError:
    def validate_order_total(submitted, calculated, tolerance=0.01):
        if abs(float(submitted) - float(calculated)) > tolerance:
            raise ValidationError("Price mismatch detected")
        return True
    
    def validate_stock_availability(product, quantity):
        if not product.in_stock or product.stock < quantity:
            raise ValidationError(f"Insufficient stock for {product.name}")
        return True
    
    def sanitize_search_query(query):
        return query.strip()[:100] if query else ""


def store(request):
    query = sanitize_search_query(request.GET.get('q', ''))
    category = request.GET.get('category', '')
    page_number = request.GET.get('page', 1)
    sort_by = request.GET.get('sort', '-created_at')
    
    products = Product.objects.all()
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if category:
        products = products.filter(category=category)
    
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'popular':
        products = products.order_by('-views')
    else:
        products = products.order_by('-created_at')
    
    paginator = Paginator(products, 12)
    products_page = paginator.get_page(page_number)
    
    categories = Product.objects.values_list('category', flat=True).distinct()

    context = {
        'products': products_page,
        'query': query,
        'categories': categories,
        'selected_category': category,
        'sort_by': sort_by,
    }
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={'name': request.user.username, 'email': request.user.email}
        )
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
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={'name': request.user.username, 'email': request.user.email}
        )
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        order = cookieData['order']
        items = cookieData['items']

    if request.POST.get('make-payment-btn') == 'make-payment-btn':
        try:
            if request.user.is_authenticated:
                customer, created = Customer.objects.get_or_create(
                    user=request.user,
                    defaults={'name': request.user.username, 'email': request.user.email}
                )
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
    product.increment_views()
    
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    
    if request.user.is_authenticated:
        try:
            from .models_extended import RecentlyViewed
            RecentlyViewed.objects.update_or_create(
                user=request.user,
                product=product
            )
        except:
            pass
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)

def order_history(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/l/')
    
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={'name': request.user.username, 'email': request.user.email}
    )
    orders = Order.objects.filter(customer=customer, complete=True).order_by('-date_ordered')
    
    # Clean up any order items with deleted products
    for order in orders:
        order.orderitem_set.filter(product__isnull=True).delete()
    
    context = {'orders': orders}
    return render(request, 'store/order_history.html', context)

def cancelled(request):
    return render(request, 'store/cancelled.html')

@require_POST
def updateItem(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=401)
    
    try:
        data = json.loads(request.body)
        productId = data.get('productId')
        action = data.get('action')
        
        if not productId or not action:
            return JsonResponse({"error": "Invalid request"}, status=400)

        with transaction.atomic():
            customer, created = Customer.objects.get_or_create(
                user=request.user,
                defaults={'name': request.user.username, 'email': request.user.email}
            )
            product = Product.objects.select_for_update().get(id=productId)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

            if action == 'add':
                new_quantity = orderItem.quantity + 1
                try:
                    validate_stock_availability(product, new_quantity)
                    orderItem.quantity = new_quantity
                except Exception as e:
                    return JsonResponse({"error": str(e)}, status=400)
            elif action == 'remove':
                orderItem.quantity = max(0, orderItem.quantity - 1)

            if orderItem.quantity <= 0:
                orderItem.delete()
                return JsonResponse({"success": True, "message": "Item removed"})
            else:
                orderItem.save()
                return JsonResponse({"success": True, "message": "Item updated", "quantity": orderItem.quantity})
                
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_POST
def processOrder(request):
    try:
        data = json.loads(request.body)
        
        with transaction.atomic():
            if request.user.is_authenticated:
                customer, created = Customer.objects.get_or_create(
                    user=request.user,
                    defaults={'name': request.user.username, 'email': request.user.email}
                )
                order, created = Order.objects.get_or_create(customer=customer, complete=False)
            else:
                name = data['form']['name']
                email = data['form']['email']
                cookieData = cookieCart(request)
                items = cookieData['items']

                customer, created = Customer.objects.get_or_create(
                    email=email,
                    user=None,
                    defaults={'name': name}
                )
                if not created:
                    customer.name = name
                    customer.save()

                order = Order.objects.create(
                    customer=customer,
                    complete=False,
                )

                for item in items:
                    product = Product.objects.get(id=item['product']['id'])
                    OrderItem.objects.create(
                        product=product,
                        order=order,
                        quantity=item['quantity']
                    )

            submitted_total = float(data['form']['total'])
            try:
                validate_order_total(submitted_total, order.get_cart_total)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
            
            order.transaction_id = Order.generate_transaction_id()
            order.complete = True
            order.status = 'processing'
            order.save()
            
            for item in order.orderitem_set.all():
                product = item.product
                product.stock -= item.quantity
                product.save()
            
            if customer.email:
                send_order_confirmation_email(customer.email, order)

            if order.shipping:
                ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode'],
                )

            return JsonResponse({"success": True, "message": "Payment processed"})
            
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)