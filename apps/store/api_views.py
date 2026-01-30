"""API views for enhanced features"""
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import transaction
import json

@login_required
@require_POST
def add_review(request):
    """Add product review"""
    try:
        from .models_extended import ProductReview
        from .models import Product, Order, OrderItem
        
        data = json.loads(request.body)
        product_id = data.get('product_id')
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        if not product_id or not rating:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        product = Product.objects.get(id=product_id)
        
        # Check if user purchased this product
        verified = OrderItem.objects.filter(
            order__customer__user=request.user,
            order__complete=True,
            product=product
        ).exists()
        
        review, created = ProductReview.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                'rating': rating,
                'comment': comment,
                'verified_purchase': verified
            }
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Review added successfully',
            'verified': verified
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def toggle_wishlist(request):
    """Add/remove product from wishlist"""
    try:
        from .models_extended import Wishlist
        from .models import Product
        
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        if not product_id:
            return JsonResponse({'error': 'Product ID required'}, status=400)
        
        product = Product.objects.get(id=product_id)
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product)
        
        if wishlist_item.exists():
            wishlist_item.delete()
            return JsonResponse({'success': True, 'action': 'removed'})
        else:
            Wishlist.objects.create(user=request.user, product=product)
            return JsonResponse({'success': True, 'action': 'added'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_wishlist(request):
    """Get user's wishlist"""
    try:
        from .models_extended import Wishlist
        
        wishlist = Wishlist.objects.filter(user=request.user).select_related('product')
        items = [{
            'id': item.id,
            'product_id': item.product.id,
            'product_name': item.product.name,
            'product_price': item.product.price,
            'product_image': item.product.imageURL,
            'added_at': item.added_at.isoformat()
        } for item in wishlist]
        
        return JsonResponse({'wishlist': items})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
def subscribe_newsletter(request):
    """Subscribe to newsletter"""
    try:
        from .models_extended import Newsletter
        
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'error': 'Email required'}, status=400)
        
        newsletter, created = Newsletter.objects.get_or_create(email=email)
        
        if created:
            return JsonResponse({'success': True, 'message': 'Subscribed successfully'})
        else:
            return JsonResponse({'success': True, 'message': 'Already subscribed'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
