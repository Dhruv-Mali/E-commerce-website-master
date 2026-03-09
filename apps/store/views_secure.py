"""Secure views with input validation and protection against common attacks"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.utils.html import escape
import json
import logging

logger = logging.getLogger(__name__)

from .utils import cookieCart, create_razorpay_order, verify_razorpay_signature, send_order_confirmation_email
from .models import Product, Customer, Order, OrderItem, ShippingAddress

# Input Validators
def sanitize_input(value, max_length=100):
    """Sanitize user input to prevent XSS"""
    if not value:
        return ""
    value = str(value).strip()[:max_length]
    return escape(value)

def validate_email(email):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number"""
    import re
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None

@staff_member_required(login_url='/l/')
def admin_dashboard(request):
    """Admin dashboard with metrics"""
    try:
        context = {
            'total_products': Product.objects.count(),
            'total_orders': Order.objects.filter(complete=True).count(),
            'total_customers': Customer.objects.count(),
            'pending_orders': Order.objects.filter(complete=False).count(),
        }
        return render(request, 'admin/dashboard.html', context)
    except Exception as e:
        logger.error(f"Admin dashboard error: {str(e)}")
        messages.error(request, "Error loading dashboard")
        return redirect('store')

@require_http_methods(["GET"])
def landing(request):
    """Landing page"""
    return render(request, 'store/landing.html')

@require_http_methods(["GET"])
def store(request):
    """Product listing with search and filtering"""
    try:
        query = sanitize_input(request.GET.get('q', ''), 100)
        category = sanitize_input(request.GET.get('category', ''), 50)
        page_number = request.GET.get('page', 1)
        sort_by = sanitize_input(request.GET.get('sort', '-created_at'), 20)
        
        products = Product.objects.all()
        
        if query:
            products = products.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            )
        
        if category:
            products = products.filter(category=category)
        
        # Whitelist sort options
        valid_sorts = ['-created_at', 'price', '-price', '-views']
        if sort_by not in valid_sorts:
            sort_by = '-created_at'
        products = products.order_by(sort_by)
        
        paginator = Paginator(products, 12)
        products_page = paginator.get_page(page_number)
        categories = Product.objects.values_list('category', flat=True).distinct()
        
        context = {
            'products': products_page,
            'query': query,
            'categories': categories,
            'selected_category': category,
            'sort_by': sort_by,
            'total_products': products.count(),
        }
        return render(request, 'store/store.html', context)
    except Exception as e:
        logger.error(f"Store view error: {str(e)}")
        messages.error(request, "Error loading products")
        return redirect('landing')

@require_http_methods(["GET"])
def cart(request):
    """Shopping cart view"""
    try:
        if request.user.is_authenticated:
            customer, _ = Customer.objects.get_or_create(
                user=request.user,
                defaults={'name': request.user.username, 'email': request.user.email}
            )
            order = Order.objects.filter(customer=customer, complete=False).first()
            if not order:
                order = Order.objects.create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        else:
            cookieData = cookieCart(request)
            items = cookieData['items']
            order = cookieData['order']
        
        context = {'items': items, 'order': order}
        return render(request, 'store/cart.html', context)
    except Exception as e:
        logger.error(f"Cart view error: {str(e)}")
        messages.error(request, "Error loading cart")
        return redirect('store')

@require_http_methods(["GET", "POST"])
@csrf_protect
def checkout(request):
    """Checkout with payment processing"""
    try:
        if request.user.is_authenticated:
            customer, _ = Customer.objects.get_or_create(
                user=request.user,
                defaults={'name': request.user.username, 'email': request.user.email}
            )
            order = Order.objects.filter(customer=customer, complete=False).first()
            if not order:
                order = Order.objects.create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        else:
            cookieData = cookieCart(request)
            items = cookieData['items']
            order = cookieData['order']
        
        razorpay_order_id = None
        
        if request.method == 'POST' and request.POST.get('make-payment-btn'):
            try:
                # Validate inputs
                email = sanitize_input(request.POST.get('email', ''), 255)
                name = sanitize_input(request.POST.get('name', ''), 100)
                address = sanitize_input(request.POST.get('address', ''), 255)
                city = sanitize_input(request.POST.get('city', ''), 100)
                state = sanitize_input(request.POST.get('state', ''), 100)
                zipcode = sanitize_input(request.POST.get('zipcode', ''), 20)
                
                if not email or not validate_email(email):
                    messages.error(request, 'Valid email is required')
                    return render(request, 'store/checkout.html', {'items': items, 'order': order})
                
                if not name:
                    messages.error(request, 'Name is required')
                    return render(request, 'store/checkout.html', {'items': items, 'order': order})
                
                # Create Razorpay order
                total_amount = order.get_cart_total if hasattr(order, 'get_cart_total') else 0
                razorpay_order = create_razorpay_order(int(total_amount * 100))
                
                if razorpay_order:
                    razorpay_order_id = razorpay_order['id']
                    request.session['pending_order_id'] = order.id
                    request.session['razorpay_order_id'] = razorpay_order_id
                    request.session['order_data'] = {
                        'name': name,
                        'email': email,
                        'address': address,
                        'city': city,
                        'state': state,
                        'zipcode': zipcode
                    }
                else:
                    messages.error(request, 'Payment gateway error')
            except Exception as e:
                logger.error(f"Checkout error: {str(e)}")
                messages.error(request, 'Error processing checkout')
        
        context = {
            'items': items,
            'order': order,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'razorpay_amount': int(order.get_cart_total * 100) if hasattr(order, 'get_cart_total') else 0,
        }
        return render(request, 'store/checkout.html', context)
    except Exception as e:
        logger.error(f"Checkout view error: {str(e)}")
        messages.error(request, "Error loading checkout")
        return redirect('cart')

@require_http_methods(["GET"])
def product_detail(request, pk):
    """Product detail view"""
    try:
        product = get_object_or_404(Product, id=pk)
        product.increment_views()
        
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:4]
        
        context = {
            'product': product,
            'related_products': related_products,
        }
        return render(request, 'store/product_detail.html', context)
    except Exception as e:
        logger.error(f"Product detail error: {str(e)}")
        messages.error(request, "Product not found")
        return redirect('store')

@require_http_methods(["GET"])
def order_history(request):
    """User order history"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        customer, _ = Customer.objects.get_or_create(
            user=request.user,
            defaults={'name': request.user.username, 'email': request.user.email}
        )
        orders = Order.objects.filter(
            customer=customer,
            complete=True,
            razorpay_payment_id__isnull=False
        ).order_by('-date_ordered')
        
        context = {'orders': orders}
        return render(request, 'store/order_history.html', context)
    except Exception as e:
        logger.error(f"Order history error: {str(e)}")
        messages.error(request, "Error loading orders")
        return redirect('store')

@require_http_methods(["GET"])
def wishlist(request):
    """Wishlist view"""
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'store/wishlist.html')

@require_http_methods(["GET"])
def payment_cancelled(request):
    """Payment cancelled handler"""
    messages.warning(request, 'Payment was cancelled. Your cart is still saved.')
    return redirect('checkout')

@require_POST
@csrf_protect
def payment_success(request):
    """Payment success handler with signature verification"""
    razorpay_payment_id = sanitize_input(request.POST.get('razorpay_payment_id', ''), 100)
    razorpay_order_id = sanitize_input(request.POST.get('razorpay_order_id', ''), 100)
    razorpay_signature = sanitize_input(request.POST.get('razorpay_signature', ''), 255)
    
    if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
        logger.warning("Invalid payment data received")
        messages.error(request, 'Invalid payment data.')
        return redirect('store')
    
    try:
        verify_razorpay_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature,
        })
        
        pending_order_id = request.session.get('pending_order_id')
        
        if not pending_order_id:
            logger.warning("Order session expired")
            messages.warning(request, 'Order session expired.')
            return redirect('store')
        
        with transaction.atomic():
            order = Order.objects.filter(id=pending_order_id, complete=False).first()
            
            if not order:
                logger.warning(f"Order {pending_order_id} not found")
                messages.warning(request, 'Order not found.')
                return redirect('store')
            
            order_data = request.session.get('order_data', {})
            
            order.transaction_id = Order.generate_transaction_id()
            order.razorpay_payment_id = razorpay_payment_id
            order.complete = True
            order.status = 'processing'
            order.save()
            
            for item in order.orderitem_set.all():
                if item.product:
                    try:
                        item.product.reduce_stock(item.quantity)
                    except Exception as e:
                        logger.error(f"Stock reduction error: {str(e)}")
            
            if order_data.get('address'):
                try:
                    ShippingAddress.objects.create(
                        customer=order.customer,
                        order=order,
                        address=order_data.get('address', ''),
                        city=order_data.get('city', ''),
                        state=order_data.get('state', ''),
                        zipcode=order_data.get('zipcode', '')
                    )
                except Exception as e:
                    logger.error(f"Shipping address error: {str(e)}")
            
            if order.customer.email:
                try:
                    send_order_confirmation_email(order.customer.email, order)
                except Exception as e:
                    logger.error(f"Email error: {str(e)}")
            
            request.session.pop('pending_order_id', None)
            request.session.pop('razorpay_order_id', None)
            request.session.pop('order_data', None)
            
            response = render(request, 'store/order_success.html', {'order': order})
            response.set_cookie('cart', '{}', max_age=0)
            
            return response
            
    except Exception as e:
        logger.error(f"Payment verification error: {str(e)}")
        messages.error(request, 'Payment verification failed.')
        return redirect('store')

@require_POST
@csrf_protect
def updateItem(request):
    """Update cart item with validation"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=401)
    
    try:
        data = json.loads(request.body)
        productId = data.get('productId')
        action = data.get('action')
        
        if not productId or not action:
            return JsonResponse({"error": "Invalid request"}, status=400)
        
        if action not in ['add', 'remove']:
            return JsonResponse({"error": "Invalid action"}, status=400)
        
        with transaction.atomic():
            customer, _ = Customer.objects.get_or_create(
                user=request.user,
                defaults={'name': request.user.username, 'email': request.user.email}
            )
            product = Product.objects.select_for_update().get(id=productId)
            order = Order.objects.filter(customer=customer, complete=False).first()
            if not order:
                order = Order.objects.create(customer=customer, complete=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
            
            if action == 'add':
                if orderItem.quantity >= product.stock:
                    return JsonResponse({"error": "Insufficient stock"}, status=400)
                orderItem.quantity += 1
            elif action == 'remove':
                orderItem.quantity = max(0, orderItem.quantity - 1)
            
            if orderItem.quantity <= 0:
                orderItem.delete()
                return JsonResponse({"success": True, "message": "Item removed"})
            else:
                orderItem.save()
                return JsonResponse({"success": True, "quantity": orderItem.quantity})
                
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        logger.error(f"Update item error: {str(e)}")
        return JsonResponse({"error": "Error updating item"}, status=500)
