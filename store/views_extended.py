from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models_extended import Wishlist, ProductReview, Newsletter
from .models import Product
import json

@login_required
@require_POST
def add_to_wishlist(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = Product.objects.get(id=product_id)
        
        wishlist, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if created:
            return JsonResponse({'success': True, 'message': 'Added to wishlist'})
        else:
            wishlist.delete()
            return JsonResponse({'success': True, 'message': 'Removed from wishlist'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    context = {'wishlist_items': wishlist_items}
    return render(request, 'store/wishlist.html', context)

@login_required
@require_POST
def add_review(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        data = json.loads(request.body)
        rating = int(data.get('rating'))
        comment = data.get('comment', '')
        
        review, created = ProductReview.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        return JsonResponse({'success': True, 'message': 'Review submitted'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_POST
def subscribe_newsletter(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        newsletter, created = Newsletter.objects.get_or_create(email=email)
        
        if created:
            return JsonResponse({'success': True, 'message': 'Subscribed successfully'})
        else:
            return JsonResponse({'success': True, 'message': 'Already subscribed'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def recently_viewed(request):
    from .models_extended import RecentlyViewed
    recent = RecentlyViewed.objects.filter(user=request.user).select_related('product')[:10]
    context = {'recent_products': recent}
    return render(request, 'store/recently_viewed.html', context)
