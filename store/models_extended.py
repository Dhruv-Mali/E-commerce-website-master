from django.db import models
from django.contrib.auth.models import User
from .models import Product, Customer

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']
        indexes = [models.Index(fields=['product', '-created_at'])]
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.IntegerField(default=0)
    discount_amount = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    min_purchase = models.IntegerField(default=0)
    usage_limit = models.IntegerField(default=1)
    used_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.code
    
    def is_valid(self):
        from django.utils import timezone
        return (self.active and 
                self.valid_from <= timezone.now() <= self.valid_to and
                self.used_count < self.usage_limit)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)  # e.g., "Size", "Color"
    value = models.CharField(max_length=100)  # e.g., "Large", "Red"
    price_adjustment = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('product', 'name', 'value')
    
    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"

class RecentlyViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"{self.user.username} viewed {self.product.name}"

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email
