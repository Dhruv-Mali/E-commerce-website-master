from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
import json
import datetime
import random
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

from .utils import cookieCart, product_sales_pipeline, send_order_confirmation_email
from .models import Product, Customer, Order, OrderItem, ShippingAddress

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

# Custom Admin Views
@staff_member_required
def admin_dashboard(request):
    context = {
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.filter(complete=True).count(),
        'total_customers': Customer.objects.count(),
        'pending_orders': Order.objects.filter(complete=False).count(),
    }
    return render(request, 'admin/dashboard.html', context)

@staff_member_required
def admin_products(request):
    products = Product.objects.all().order_by('-created_at')
    context = {'products': products}
    return render(request, 'admin/products.html', context)

@staff_member_required
def admin_add_product(request):
    from .forms import ProductForm
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('admin_products')
    else:
        form = ProductForm()
    
    context = {'form': form}
    return render(request, 'admin/add_product.html', context)

@staff_member_required
def admin_edit_product(request, product_id):
    from .forms import ProductForm
    
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'product': product}
    return render(request, 'admin/edit_product.html', context)

@staff_member_required
def admin_delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('admin_products')
    
    context = {'product': product}
    return render(request, 'admin/delete_product.html', context)

@staff_member_required
def admin_orders(request):
    # ONLY show completed orders (paid orders)
    orders = Order.objects.filter(
        complete=True,
        stripe_payment_intent__isnull=False
    ).order_by('-date_ordered')
    
    if request.method == 'POST':
        # Handle order status updates
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        if order_id and new_status:
            order = get_object_or_404(Order, id=order_id, complete=True)
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.transaction_id} status updated to {new_status}!')
            return redirect('admin_orders')
    
    context = {'orders': orders}
    return render(request, 'admin/orders.html', context)

def landing(request):
    return render(request, 'store/landing.html')

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
        'total_products': products.count(),
    }
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={'name': request.user.username, 'email': request.user.email}
        )
        # Get the most recent incomplete order or create a new one
        order = Order.objects.filter(customer=customer, complete=False).first()
        if not order:
            order = Order.objects.create(customer=customer, complete=False)
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
        order = Order.objects.filter(customer=customer, complete=False).first()
        if not order:
            order = Order.objects.create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        order = cookieData['order']
        items = cookieData['items']

    if request.method == 'POST' and request.POST.get('make-payment-btn'):
        try:
            if request.user.is_authenticated:
                order_id = order.id
                total_amount = order.get_cart_total
            else:
                # Create guest customer and order before payment
                guest_email = request.POST.get('email', '')
                guest_name = request.POST.get('name', '')
                
                if not guest_email:
                    messages.error(request, 'Email is required for checkout.')
                    return render(request, 'store/checkout.html', {'items': items, 'order': order})
                
                customer, created = Customer.objects.get_or_create(
                    email=guest_email,
                    user=None,
                    defaults={'name': guest_name}
                )
                
                # Create order for guest
                order_obj = Order.objects.create(customer=customer, complete=False)
                
                # Add items from cookie cart to order
                for item in items:
                    product = Product.objects.get(id=item['product']['id'])
                    OrderItem.objects.create(
                        product=product,
                        order=order_obj,
                        quantity=item['quantity']
                    )
                
                order_id = order_obj.id
                total_amount = order_obj.get_cart_total
            
            stripe_url = product_sales_pipeline(order_id, int(total_amount * 100), request)
            
            if stripe_url:
                # Store order data in session for processing after payment
                request.session['pending_order_id'] = order_id
                request.session['order_data'] = {
                    'name': request.POST.get('name', ''),
                    'email': request.POST.get('email', ''),
                    'address': request.POST.get('address', ''),
                    'city': request.POST.get('city', ''),
                    'state': request.POST.get('state', ''),
                    'zipcode': request.POST.get('zipcode', '')
                }
                return HttpResponseRedirect(stripe_url)
            else:
                messages.error(request, 'Payment gateway error. Please try again.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        
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
    # ONLY show completed orders with successful payment
    orders = Order.objects.filter(
        customer=customer,
        complete=True,
        stripe_payment_intent__isnull=False
    ).order_by('-date_ordered')
    
    # Clean up any order items with deleted products
    for order in orders:
        order.orderitem_set.filter(product__isnull=True).delete()
    
    context = {'orders': orders}
    return render(request, 'store/order_history.html', context)

def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'store/wishlist.html')

def payment_cancelled(request):
    messages.warning(request, 'Payment was cancelled. Your cart is still saved.')
    return redirect('checkout')

def payment_success(request):
    session_id = request.GET.get('session_id')
    
    if not session_id:
        messages.error(request, 'Invalid payment session.')
        return redirect('store')
    
    try:
        # Verify payment with Stripe
        stripe_session = stripe.checkout.Session.retrieve(session_id)
        
        if stripe_session.payment_status != 'paid':
            messages.error(request, 'Payment verification failed.')
            return redirect('checkout')
        
        # Get pending order from session
        pending_order_id = request.session.get('pending_order_id')
        
        if not pending_order_id:
            messages.warning(request, 'Order session expired. Please contact support if payment was deducted.')
            return redirect('store')
        
        with transaction.atomic():
            order = Order.objects.filter(id=pending_order_id, complete=False).first()
            
            if not order:
                messages.warning(request, 'Order not found. Please contact support if payment was deducted.')
                return redirect('store')
            
            # Get order data from session
            order_data = request.session.get('order_data', {})
            
            # Mark order as complete
            order.transaction_id = Order.generate_transaction_id()
            order.stripe_payment_intent = session_id
            order.complete = True
            order.status = 'processing'
            order.save()
            
            # Reduce stock
            for item in order.orderitem_set.all():
                if item.product:
                    try:
                        item.product.reduce_stock(item.quantity)
                    except Exception as e:
                        pass  # Continue even if stock update fails
            
            # Save shipping address
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
                    pass  # Continue even if shipping save fails
            
            # Send confirmation email
            if order.customer.email:
                try:
                    send_order_confirmation_email(order.customer.email, order)
                except Exception as e:
                    pass  # Continue even if email fails
            
            # Clear session data
            request.session.pop('pending_order_id', None)
            request.session.pop('order_data', None)
            
            # Clear cart cookie
            response = render(request, 'store/order_success.html', {'order': order})
            response.set_cookie('cart', '{}', max_age=0)
            
            return response
            
    except stripe.error.StripeError as e:
        messages.error(request, f'Payment verification error: {str(e)}')
        return redirect('store')
    except Exception as e:
        messages.error(request, f'Error processing order: {str(e)}')
        return redirect('store')

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
            # Get the most recent incomplete order or create a new one
            order = Order.objects.filter(customer=customer, complete=False).first()
            if not order:
                order = Order.objects.create(customer=customer, complete=False)
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
                # Get the most recent incomplete order or create a new one
                order = Order.objects.filter(customer=customer, complete=False).first()
                if not order:
                    order = Order.objects.create(customer=customer, complete=False)
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