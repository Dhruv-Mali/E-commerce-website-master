import os

filepath = r'c:\Users\dhruv\E-commerce-website-master-final\apps\store\templates\store\checkout.html'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

css = """<style>
    .checkout-row {
        margin: 0;
    }

    .checkout-card {
        background: var(--c-surface);
        border: 1px solid var(--c-border);
        border-radius: 20px;
        backdrop-filter: blur(12px);
        box-shadow: var(--shadow-glow);
    }

    .checkout-form-body,
    .checkout-summary-body {
        padding: 2rem;
    }

    .checkout-title {
        color: var(--text-main);
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .checkout-section-title {
        color: var(--c-secondary);
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .checkout-input {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--c-border);
        color: var(--text-main);
        padding: 0.8rem 1rem;
        font-size: 1rem;
        border-radius: 12px;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .checkout-input:focus {
        background: rgba(0, 0, 0, 0.2);
        border-color: var(--c-primary);
        color: var(--text-main);
        box-shadow: 0 0 0 4px rgba(123, 97, 255, 0.1);
        outline: none;
    }
    
    .checkout-input::placeholder {
        color: var(--text-muted);
        opacity: 0.7;
    }

    .btn-payment {
        padding: 1rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--c-secondary), var(--c-primary));
        color: white;
        border: none;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(123, 97, 255, 0.3);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        letter-spacing: 0.5px;
    }

    .btn-payment:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(123, 97, 255, 0.5);
        color: white;
    }

    .order-items {
        max-height: 400px;
        overflow-y: auto;
        padding-right: 0.5rem;
    }
    
    .order-items::-webkit-scrollbar {
        width: 6px;
    }
    
    .order-items::-webkit-scrollbar-thumb {
        background: rgba(123, 97, 255, 0.3);
        border-radius: 10px;
    }

    .order-item {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px;
        padding: 1rem !important;
        transition: all 0.3s ease;
    }
    
    .order-item:hover {
        background: rgba(123, 97, 255, 0.05);
        transform: translateX(5px);
    }

    .order-item-img {
        width: 60px;
        height: 60px;
        object-fit: cover;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }

    .order-item-name {
        color: var(--text-main);
        font-size: 1.05rem;
        font-weight: 600;
    }

    .order-item-qty {
        font-size: 0.85rem;
        color: var(--c-secondary) !important;
    }

    .order-item-price {
        color: var(--text-main);
        font-size: 1.1rem;
    }

    .summary-row {
        padding: 0.5rem 0;
    }

    .summary-label {
        color: var(--text-muted);
        font-size: 1rem;
        font-weight: 500;
    }
    
    .summary-value {
        color: var(--text-main);
        font-size: 1.05rem;
    }

    .total-label {
        color: var(--text-main);
        font-size: 1.3rem;
        font-weight: 800;
    }
    
    .total-value {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--c-secondary), var(--c-primary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .checkout-alert {
        background: rgba(123, 97, 255, 0.1);
        border: 1px solid rgba(123, 97, 255, 0.3);
        color: var(--c-secondary);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .back-btn {
        border-radius: 20px;
        padding: 0.4rem 1rem;
        border: 1px solid var(--glass-border);
        color: var(--text-muted);
        background: var(--glass-bg);
        transition: all 0.3s;
    }
    
    .back-btn:hover {
        background: rgba(255,255,255,0.05);
        color: var(--text-main);
        border-color: var(--c-border);
    }

    /* Tablet Responsive */
    @media (max-width: 992px) {
        .checkout-title {
            font-size: 1.35rem;
        }

        .checkout-section-title {
            font-size: 1rem;
        }
    }

    /* Mobile Responsive */
    @media (max-width: 768px) {
        .checkout-row {
            margin: 0 -0.5rem;
        }

        .checkout-form-body,
        .checkout-summary-body {
            padding: 1.5rem;
        }

        .checkout-title {
            font-size: 1.25rem;
        }

        .checkout-section-title {
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
        }

        .checkout-input {
            padding: 0.75rem;
            font-size: 0.95rem;
        }

        .btn-payment {
            padding: 0.85rem 1.25rem;
            font-size: 1rem;
        }

        .back-btn {
            font-size: 0.85rem;
            padding: 0.5rem 1rem;
        }

        .order-items {
            max-height: 280px;
        }

        .order-item-img {
            width: 50px;
            height: 50px;
        }

        .order-item-name {
            font-size: 0.95rem;
        }

        .order-item-qty {
            font-size: 0.8rem;
        }

        .order-item-price {
            font-size: 1rem;
        }

        .summary-label,
        .summary-value {
            font-size: 0.9rem;
        }

        .total-label {
            font-size: 1.15rem;
        }
        
        .total-value {
            font-size: 1.3rem;
        }

        .checkout-alert {
            font-size: 0.9rem;
            padding: 0.75rem;
        }
    }

    /* Small Mobile */
    @media (max-width: 576px) {

        .checkout-form-body,
        .checkout-summary-body {
            padding: 1rem;
        }

        .checkout-title {
            font-size: 1.1rem;
        }

        .checkout-section-title {
            font-size: 0.9rem;
        }

        .checkout-input {
            padding: 0.7rem;
            font-size: 0.9rem;
        }

        .btn-payment {
            padding: 0.75rem 1rem;
            font-size: 0.95rem;
        }

        .order-items {
            max-height: 240px;
        }

        .order-item-img {
            width: 45px;
            height: 45px;
        }

        .order-item-name {
            font-size: 0.85rem;
        }

        .order-item-qty {
            font-size: 0.75rem;
        }

        .order-item-price {
            font-size: 0.9rem;
        }

        .summary-label,
        .summary-value {
            font-size: 0.85rem;
        }

        .total-label {
            font-size: 1.05rem;
        }
        
        .total-value {
            font-size: 1.2rem;
        }
    }
</style>
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines[:334])
    f.write(css)
    f.write('\n{% endblock content %}\n')

print('Success')
