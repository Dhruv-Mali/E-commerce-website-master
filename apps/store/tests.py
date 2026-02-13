"""Unit tests for store app"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.store.models import Product, Customer, Order, OrderItem
from decimal import Decimal

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            price=1000,
            stock=10,
            category="Electronics"
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 1000)
        self.assertTrue(self.product.in_stock)

    def test_reduce_stock(self):
        initial_stock = self.product.stock
        self.product.reduce_stock(5)
        self.assertEqual(self.product.stock, initial_stock - 5)

    def test_insufficient_stock(self):
        with self.assertRaises(Exception):
            self.product.reduce_stock(20)

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'password')
        self.customer, _ = Customer.objects.get_or_create(
            user=self.user,
            defaults={'name': 'Test User', 'email': 'test@test.com'}
        )
        self.order = Order.objects.create(customer=self.customer)
        self.product = Product.objects.create(name="Test Product", price=1000, stock=10)

    def test_order_creation(self):
        self.assertFalse(self.order.complete)
        self.assertEqual(self.order.customer, self.customer)

    def test_cart_total(self):
        OrderItem.objects.create(order=self.order, product=self.product, quantity=2)
        self.assertEqual(self.order.get_cart_total, 2000)

    def test_cart_items_count(self):
        OrderItem.objects.create(order=self.order, product=self.product, quantity=3)
        self.assertEqual(self.order.get_cart_items, 3)

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'password')
        # Ensure no duplicate Customer is created during tests
        Customer.objects.get_or_create(user=self.user, defaults={'name': self.user.username, 'email': self.user.email})
        self.product = Product.objects.create(name="Test Product", price=1000, stock=10)

    def test_store_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        response = self.client.get(f'/product/{self.product.id}/')
        self.assertEqual(response.status_code, 200)

    def test_cart_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post('/update-item/', 
            data='{"productId": ' + str(self.product.id) + ', "action": "add"}',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
