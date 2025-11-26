from .utils import cookieCart
from .models import Order

def cart_context(request):
    """Add cart items count to all templates"""
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
    
    return {'cartItems': cartItems}
