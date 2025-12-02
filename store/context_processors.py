from .utils import cookieCart
from .models import Order, Customer

def cart_context(request):
    """Add cart items count to all templates"""
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer, created = Customer.objects.get_or_create(
                user=request.user,
                defaults={'name': request.user.username, 'email': request.user.email}
            )
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
    
    return {'cartItems': cartItems}
