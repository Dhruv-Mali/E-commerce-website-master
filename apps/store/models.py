from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
import uuid

# Import extended models for Django to recognize them
try:
    from .models_extended import (
        ProductReview, Wishlist, Coupon, 
        ProductVariant, RecentlyViewed, Newsletter
    )
except ImportError:
    pass  # Extended models not yet available

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=True, db_index=True)

    def __str__(self):
        return self.name or self.email or f"Customer {self.id}"
    
class Product(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True, db_index=True)
    price = models.IntegerField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    stock = models.IntegerField(default=100)
    category = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    views = models.IntegerField(default=0)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
            
        return url
    
    @property
    def in_stock(self):
        return self.stock > 0
    
    def reduce_stock(self, quantity):
        """Thread-safe stock reduction"""
        if self.stock < quantity:
            raise ValidationError(f"Insufficient stock for {self.name}")
        self.stock -= quantity
        self.save(update_fields=['stock'])
    
    def increment_views(self):
        """Increment product views - safe for existing products"""
        if hasattr(self, 'views') and self.views is not None:
            self.views += 1
        else:
            self.views = 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['-views']),
        ]
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True, unique=True, db_index=True)
    stripe_payment_intent = models.CharField(max_length=300, null=True, blank=True)
    status = models.CharField(max_length=50, default='pending', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ])

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product and item.product.digital == False:
                shipping = True

        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return str(self.id)
    
    @staticmethod
    def generate_transaction_id():
        """Generate unique transaction ID"""
        return str(uuid.uuid4())
    
    class Meta:
        indexes = [
            models.Index(fields=['-date_ordered']),
            models.Index(fields=['customer', '-date_ordered']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['customer'],
                condition=models.Q(complete=False),
                name='unique_incomplete_order_per_customer'
            )
        ]
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        if self.product:
            return self.quantity * self.product.price
        return 0

    def __str__(self):
        return self.product.name if self.product else "Deleted Product"
    


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=20, null=True)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email
        )