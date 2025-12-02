from django.urls import path
from . import views_extended, webhooks

urlpatterns = [
    path('wishlist/', views_extended.wishlist_view, name='wishlist'),
    path('wishlist/add/', views_extended.add_to_wishlist, name='add_to_wishlist'),
    path('review/<int:product_id>/', views_extended.add_review, name='add_review'),
    path('newsletter/subscribe/', views_extended.subscribe_newsletter, name='subscribe_newsletter'),
    path('recently-viewed/', views_extended.recently_viewed, name='recently_viewed'),
    path('webhook/stripe/', webhooks.stripe_webhook, name='stripe_webhook'),
]
