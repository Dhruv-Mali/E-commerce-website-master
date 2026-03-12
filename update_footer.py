import os

filepath = r'c:\Users\dhruv\E-commerce-website-master-final\core\templates\footer.html'
html = """<!-- Compact Glassmorphic Footer -->
<footer class="footer mt-auto" style="background: var(--c-surface); color: var(--text-muted); border-top: 1px solid var(--c-border); backdrop-filter: blur(10px); z-index: 10;">
    <div class="container-fluid px-4 py-3">
        <div class="row align-items-center mb-0 g-3">
            <!-- Brand -->
            <div class="col-12 col-md-4 text-center text-md-start mb-0">
                <a href="{% url 'landing' %}" class="text-decoration-none d-flex align-items-center justify-content-center justify-content-md-start gap-2">
                    <div class="rounded-circle d-flex align-items-center justify-content-center" style="width: 24px; height: 24px; background: linear-gradient(135deg, var(--c-secondary), var(--c-primary)); color: white; font-size: 0.7rem;">⚡</div>
                    <span class="fw-bold" style="color: var(--text-main); letter-spacing: 0.5px;">ElectroMart</span>
                </a>
            </div>
            
            <!-- Quick Links & Socials -->
            <div class="col-12 col-md-4 text-center mb-0">
                <div class="d-flex justify-content-center align-items-center gap-3">
                    <a href="{% url 'store' %}" class="footer-link">Store</a>
                    <a href="{% url 'cart' %}" class="footer-link">Cart</a>
                    <div style="width: 1px; height: 15px; background: var(--c-border);"></div>
                    <a href="#" class="social-icon-sm"><i class="fab fa-twitter"></i></a>
                    <a href="#" class="social-icon-sm"><i class="fab fa-instagram"></i></a>
                </div>
            </div>
            
            <!-- Copyright & Badges -->
            <div class="col-12 col-md-4 text-center text-md-end">
                <div class="d-flex align-items-center justify-content-center justify-content-md-end gap-2">
                    <span style="font-size: 0.8rem;">&copy; 2024 ElectroMart</span>
                    <span class="badge" style="background: rgba(123, 97, 255, 0.1); color: var(--c-primary); border: 1px solid rgba(123, 97, 255, 0.2);"><i class="fas fa-lock mini-icon"></i> SSL</span>
                </div>
            </div>
        </div>
    </div>
</footer>

<style>
.footer {
    width: 100%;
    margin-top: 2rem;
}

.footer-link {
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 500;
    transition: color 0.2s;
}

.footer-link:hover {
    color: var(--c-primary);
}

.social-icon-sm {
    color: var(--text-muted);
    font-size: 0.95rem;
    transition: all 0.2s;
    text-decoration: none;
}

.social-icon-sm:hover {
    color: var(--c-secondary);
    transform: translateY(-2px);
}

.mini-icon {
    font-size: 0.7rem;
}
</style>
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
print("Success")
