import os

filepath = r'c:\Users\dhruv\E-commerce-website-master-final\apps\store\templates\store\cart.html'

html_content = """{% extends 'index.html' %}
{% load static %}
{% block content %}

<style>
/* Cart Page Glass Stylings */
.cart-header-box {
    background: linear-gradient(135deg, rgba(123, 97, 255, 0.1), rgba(0, 194, 255, 0.1));
    border: 1px solid rgba(123, 97, 255, 0.3);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px rgba(123, 97, 255, 0.15);
    backdrop-filter: blur(10px);
}

.cart-item-row {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    color: var(--text-main);
}

.cart-item-row:hover {
    transform: translateY(-3px) scale(1.01);
    background: rgba(123, 97, 255, 0.05);
    border-color: rgba(123, 97, 255, 0.3);
    box-shadow: 0 5px 20px rgba(0,0,0,0.4);
}

.qty-controls {
    background: var(--glass-bg);
    padding: 0.3rem 0.5rem;
    border-radius: 20px;
    border: 1px solid var(--glass-border);
    width: fit-content;
}

.qty-controls button {
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
    color: var(--text-main);
    transition: all 0.2s;
    border: none;
}

.qty-controls button:hover {
    background: var(--c-primary);
    color: white;
}

.btn-checkout-premium {
    background: linear-gradient(135deg, var(--c-secondary), var(--c-primary));
    color: white;
    border: none;
    border-radius: 25px;
    box-shadow: 0 4px 15px rgba(123, 97, 255, 0.4);
    transition: all 0.3s;
}

.btn-checkout-premium:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(123, 97, 255, 0.6);
    color: white;
}

.btn-remove-cart {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(231, 76, 60, 0.1);
    color: #e74c3c;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(231, 76, 60, 0.3);
    transition: all 0.2s;
}

.btn-remove-cart:hover {
    background: #e74c3c;
    color: white;
    transform: scale(1.1);
    box-shadow: 0 0 15px rgba(231, 76, 60, 0.4);
}
</style>

<div class="row mb-5 mt-3">
    <div class="col-12">
        <div class="d-flex align-items-center mb-4">
            <a href="{% url 'store' %}" class="btn btn-outline-secondary btn-sm me-3" style="border-radius: 20px; padding: 0.4rem 1rem;">
                <i class="fas fa-arrow-left me-2"></i> Continue Shopping
            </a>
            <h2 class="mb-0 fw-bold" style="color: var(--text-main);">Your <span style="background: linear-gradient(135deg, var(--c-secondary), var(--c-primary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Shopping Cart</span></h2>
        </div>
        
        {% if items %}
        <!-- Premium Summary Header -->
        <div class="cart-header-box mb-4">
            <div class="d-flex flex-column flex-md-row justify-content-between align-items-center gap-4">
                <div class="d-flex gap-4 text-center text-md-start w-100 w-md-auto align-items-center justify-content-around justify-content-md-start">
                    <div>
                        <p class="text-muted mb-1 small fw-bold text-uppercase">Total Items</p>
                        <h4 class="fw-bold mb-0 text-white">{{order.get_cart_items}}</h4>
                    </div>
                    <div>
                        <p class="text-muted mb-1 small fw-bold text-uppercase">Total Amount</p>
                        <h4 class="fw-bold mb-0" style="color: var(--c-secondary);">₹{{order.get_cart_total|floatformat:0}}</h4>
                    </div>
                </div>
                <div class="w-100 w-md-auto text-center text-md-end">
                    <a href="{% url 'checkout' %}" class="btn btn-checkout-premium px-5 py-3 fw-bold w-100 fs-5">
                        <i class="fas fa-lock me-2"></i> Secure Checkout
                    </a> 
                </div>
            </div>
        </div>
        {% else %}
        <!-- Empty Cart -->
        <div class="glass-box text-center py-5 mb-5 mx-auto" style="max-width: 600px;">
            <div class="mb-4">
                <i class="fas fa-shopping-cart text-muted" style="font-size: 5rem; opacity: 0.3;"></i>
            </div>
            <h3 class="fw-bold text-white mb-3">Your cart is empty</h3>
            <p class="text-muted mb-4 fs-5">Looks like you haven't added any premium tech to your cart yet.</p>
            <a href="{% url 'store' %}" class="btn px-4 py-2" style="background: linear-gradient(135deg, var(--c-secondary), var(--c-primary)); color: white; border: none; border-radius: 25px; box-shadow: 0 4px 15px rgba(123, 97, 255, 0.4); font-weight: 600;">
                Start Browsing
            </a>
        </div>
        {% endif %}
    </div>
</div>

{% if items %}
<!-- Desktop Item List View -->
<div class="d-none d-md-block mb-5">
    <!-- Header row -->
    <div class="row text-muted small fw-bold mb-3 px-3 pb-2 text-uppercase" style="border-bottom: 1px solid var(--c-border); letter-spacing: 1px;">
        <div class="col-5">Product Details</div>
        <div class="col-2 text-center">Unit Price</div>
        <div class="col-2 text-center">Quantity</div>
        <div class="col-2 text-center">Subtotal</div>
        <div class="col-1 text-center">Action</div>
    </div>
    
    <!-- Items -->
    <div class="cart-items-container">
        {% for item in items %}
        <div class="row align-items-center mb-3 p-3 cart-item-row mx-0">
            <div class="col-5 d-flex align-items-center gap-3">
                <img src="{{item.product.imageURL}}" alt="{{item.product.name}}" class="rounded" style="width: 80px; height: 80px; object-fit: cover; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1);"/>
                <div>
                    <h6 class="mb-1 fw-bold fs-5">{{item.product.name}}</h6>
                    <span class="badge" style="background: rgba(123, 97, 255, 0.1); color: var(--c-secondary); border: 1px solid rgba(123, 97, 255, 0.3);">{{item.product.category}}</span>
                </div>
            </div>
            <div class="col-2 text-center">
                <span class="fw-medium text-muted">₹{{item.product.price|floatformat:0}}</span>
            </div>
            <div class="col-2 d-flex justify-content-center">
                <div class="qty-controls">
                    <button data-product={{item.product.id}} data-action="remove" class="p-0 update-cart"><i class="fas fa-minus fs-6"></i></button>
                    <span class="fw-bold px-3 fs-5">{{item.quantity}}</span>
                    <button data-product={{item.product.id}} data-action="add" class="p-0 update-cart"><i class="fas fa-plus fs-6"></i></button>
                </div>
            </div>
            <div class="col-2 text-center">
                <strong class="fs-5" style="color: var(--c-secondary);">₹{{item.get_total|floatformat:0}}</strong>
            </div>
            <div class="col-1 d-flex justify-content-center">
                <button data-product={{item.product.id}} data-action="remove" class="btn-remove-cart update-cart">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

<!-- Mobile Card View -->
<div class="d-md-none mobile-cart-items mb-5">
    {% for item in items %}
    <div class="cart-item-row mb-3 p-3 mx-2">
        <div class="row g-3 align-items-center">
            <div class="col-4">
                <img src="{{item.product.imageURL}}" alt="{{item.product.name}}" class="rounded w-100" style="height: 100px; object-fit: cover; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 4px 10px rgba(0,0,0,0.3);"/>
            </div>
            <div class="col-8">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                        <h6 class="mb-1 fw-bold" style="font-size: 1.1rem;">{{item.product.name}}</h6>
                        <span class="badge" style="background: rgba(123, 97, 255, 0.1); color: var(--c-secondary); border: 1px solid rgba(123, 97, 255, 0.3);">{{item.product.category}}</span>
                    </div>
                </div>
                
                <div class="d-flex justify-content-between align-items-center mb-2 mt-2">
                    <span class="text-muted small">Price:</span>
                    <strong class="text-white">₹{{item.product.price|floatformat:0}}</strong>
                </div>
                
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <span class="text-muted small">Quantity:</span>
                    <div class="qty-controls" style="padding: 0.15rem 0.3rem;">
                        <button data-product={{item.product.id}} data-action="remove" class="update-cart p-0" style="width: 24px; height: 24px;"><i class="fas fa-minus" style="font-size: 0.7rem;"></i></button>
                        <span class="fw-bold px-2 text-white">{{item.quantity}}</span>
                        <button data-product={{item.product.id}} data-action="add" class="update-cart p-0" style="width: 24px; height: 24px;"><i class="fas fa-plus" style="font-size: 0.7rem;"></i></button>
                    </div>
                </div>
                
                <div class="d-flex justify-content-between align-items-center pt-2" style="border-top: 1px solid var(--glass-border);">
                    <small class="text-muted text-uppercase fw-bold" style="font-size: 0.7rem;">Subtotal</small>
                    <strong class="fs-5" style="color: var(--c-secondary);">₹{{item.get_total|floatformat:0}}</strong>
                </div>
                
                <button data-product={{item.product.id}} data-action="remove" class="btn btn-outline-danger w-100 mt-3 update-cart" style="border-radius: 8px; padding: 0.4rem;">
                    <i class="fas fa-trash me-2"></i> Remove Item
                </button>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endif %}

{% endblock content %}
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Success')
