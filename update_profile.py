import os

filepath = r'c:\Users\dhruv\E-commerce-website-master-final\apps\loginsys\templates\loginsys\profile.html'

css = """<style>
.profile-container {
    padding: 3rem 0;
}

.profile-card {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: 20px;
    box-shadow: var(--shadow-glow);
    backdrop-filter: blur(12px);
    overflow: hidden;
    position: relative;
}

.profile-card::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at top right, rgba(123, 97, 255, 0.05), transparent 40%),
                radial-gradient(circle at bottom left, rgba(0, 194, 255, 0.05), transparent 40%);
    pointer-events: none;
    z-index: 0;
}

.profile-header, .profile-body {
    position: relative;
    z-index: 1;
}

.profile-header {
    background: rgba(123, 97, 255, 0.1);
    border-bottom: 1px solid var(--c-border);
    padding: 1.5rem 2rem;
}

.profile-title {
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--text-main);
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.profile-body {
    padding: 2.5rem;
    background: rgba(255, 255, 255, 0.01);
}

.profile-label {
    color: var(--text-muted);
    font-weight: 600;
    margin-bottom: 0.75rem;
    font-size: 0.95rem;
}

.profile-input {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--c-border);
    color: var(--text-main);
    padding: 0.85rem 1.25rem;
    font-size: 1rem;
    border-radius: 12px;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.profile-input:focus {
    background: rgba(0, 0, 0, 0.2);
    border-color: var(--c-primary);
    color: var(--text-main);
    box-shadow: 0 0 0 4px rgba(123, 97, 255, 0.1);
    outline: none;
}

.profile-input:disabled {
    background: rgba(255, 255, 255, 0.01);
    color: var(--text-muted);
    border-color: rgba(255, 255, 255, 0.05);
    cursor: not-allowed;
}

.profile-btn {
    padding: 0.85rem 2.5rem;
    font-size: 1.05rem;
    font-weight: 700;
    margin-right: 1rem;
    background: linear-gradient(135deg, var(--c-secondary), var(--c-primary));
    color: white;
    border: none;
    border-radius: 12px;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 4px 15px rgba(123, 97, 255, 0.3);
    letter-spacing: 0.5px;
}

.profile-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(123, 97, 255, 0.5);
    color: white;
}

.profile-btn-back {
    padding: 0.85rem 2rem;
    font-size: 1rem;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    color: var(--text-muted);
    background: transparent;
    transition: all 0.3s;
    font-weight: 500;
}

.profile-btn-back:hover {
    background: rgba(255,255,255,0.05);
    color: var(--text-main);
    border-color: var(--c-border);
}

/* Tablet Responsive */
@media (max-width: 992px) {
    .profile-body {
        padding: 2rem;
    }
    
    .profile-title {
        font-size: 1.4rem;
    }
}

/* Mobile Responsive */
@media (max-width: 768px) {
    .profile-container {
        padding: 1.5rem 0.5rem;
    }
    
    .profile-header {
        padding: 1.25rem 1.5rem;
    }
    
    .profile-title {
        font-size: 1.3rem;
    }
    
    .profile-body {
        padding: 1.5rem;
    }
    
    .profile-label {
        font-size: 0.9rem;
    }
    
    .profile-input {
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
    }
    
    .profile-btn,
    .profile-btn-back {
        width: 100%;
        margin-bottom: 0.75rem;
        margin-right: 0;
        padding: 0.85rem 1.5rem;
        font-size: 1rem;
    }
}

/* Small Mobile */
@media (max-width: 576px) {
    .profile-header {
        padding: 1rem;
    }
    
    .profile-title {
        font-size: 1.2rem;
    }
    
    .profile-body {
        padding: 1.25rem;
    }
    
    .profile-label {
        font-size: 0.85rem;
    }
    
    .profile-input {
        padding: 0.7rem;
        font-size: 0.9rem;
    }
    
    .profile-btn,
    .profile-btn-back {
        padding: 0.75rem 1.2rem;
        font-size: 0.95rem;
    }
}
</style>
"""

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines[:36])
    f.write(css)
    f.write('\n{% endblock %}\n')

print("Success")
