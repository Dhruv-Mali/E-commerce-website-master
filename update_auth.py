import os

login_path = r'c:\Users\dhruv\E-commerce-website-master-final\apps\loginsys\templates\loginsys\login.html'
register_path = r'c:\Users\dhruv\E-commerce-website-master-final\apps\loginsys\templates\loginsys\registerUser.html'

login_css = """<style>
  .login-card {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    box-shadow: var(--shadow-glow);
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
  }

  .login-card::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at top right, rgba(123, 97, 255, 0.05), transparent 40%),
                radial-gradient(circle at bottom left, rgba(0, 194, 255, 0.05), transparent 40%);
    pointer-events: none;
    z-index: 0;
  }

  .login-header, .login-form, .login-divider, .btn {
    position: relative;
    z-index: 1;
  }

  .login-header {
    text-align: center;
    margin-bottom: 2.5rem;
  }

  .login-title {
    color: var(--text-main);
    font-weight: 800;
    margin: 0;
    font-size: 2.2rem;
    letter-spacing: -0.5px;
  }

  .login-subtitle {
    color: var(--c-secondary);
    font-size: 1rem;
    margin-top: 0.5rem;
    margin-bottom: 0;
    font-weight: 500;
  }

  .form-label {
    color: var(--text-muted);
    font-weight: 600;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.95rem;
  }

  .form-label i {
    color: var(--c-secondary);
    font-size: 1.1rem;
  }

  .form-control {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--c-border);
    color: var(--text-main);
    padding: 0.85rem 1.25rem;
    border-radius: 12px;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    font-size: 1rem;
  }

  .form-control:focus {
    background: rgba(0, 0, 0, 0.2);
    border-color: var(--c-primary);
    color: var(--text-main);
    box-shadow: 0 0 0 4px rgba(123, 97, 255, 0.1);
    outline: none;
  }

  .form-control::placeholder {
    color: rgba(255, 255, 255, 0.3);
  }

  .btn-login {
    background: linear-gradient(135deg, var(--c-secondary), var(--c-primary));
    border: none;
    color: white;
    font-weight: 700;
    border-radius: 12px;
    padding: 0.85rem;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 4px 15px rgba(123, 97, 255, 0.3);
    letter-spacing: 0.5px;
  }

  .btn-login:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(123, 97, 255, 0.5);
    color: white;
  }

  .btn-signup {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--c-border);
    color: var(--text-main);
    font-weight: 600;
    border-radius: 12px;
    padding: 0.85rem;
    transition: all 0.3s;
  }

  .btn-signup:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
    color: white;
    border-color: var(--c-primary);
  }

  .btn-outline-secondary {
    border-radius: 12px;
    padding: 0.85rem;
    border: 1px solid rgba(255,255,255,0.1);
    color: var(--text-muted);
    background: transparent;
    transition: all 0.3s;
  }
  
  .btn-outline-secondary:hover {
    background: rgba(255,255,255,0.05);
    color: var(--text-main);
    border-color: var(--c-border);
  }

  .login-footer {
    text-align: right;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
  }

  .login-footer p {
    color: var(--text-muted);
    margin: 0;
    font-size: 0.9rem;
  }

  .login-footer a {
    color: var(--c-secondary);
    text-decoration: none;
    font-weight: 600;
    transition: color 0.3s;
  }

  .login-footer a:hover {
    color: var(--c-primary);
    text-decoration: underline;
  }

  .login-divider {
    text-align: center;
    margin: 2rem 0;
    position: relative;
    z-index: 1;
  }

  .login-divider::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--c-border), transparent);
  }

  .login-divider span {
    background: var(--c-surface);
    padding: 0 1rem;
    color: var(--text-muted);
    font-size: 0.85rem;
    position: relative;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  @media (max-width: 768px) {
    .login-card {
      padding: 2rem 1.5rem;
    }

    .login-title {
      font-size: 1.8rem;
    }
  }
</style>
"""

register_css = """<style>
.signup-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 20px;
  padding: 3rem 2.5rem;
  box-shadow: var(--shadow-glow);
  backdrop-filter: blur(12px);
  position: relative;
  overflow: hidden;
}

.signup-card::before {
  content: '';
  position: absolute;
  top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: radial-gradient(circle at top right, rgba(123, 97, 255, 0.05), transparent 40%),
              radial-gradient(circle at bottom left, rgba(0, 194, 255, 0.05), transparent 40%);
  pointer-events: none;
  z-index: 0;
}

.signup-card > form, .signup-header, .btn {
  position: relative;
  z-index: 1;
}

.signup-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.signup-title {
  color: var(--text-main);
  font-weight: 800;
  margin: 0;
  font-size: 2.2rem;
  letter-spacing: -0.5px;
}

.signup-subtitle {
  color: var(--c-secondary);
  font-size: 1rem;
  margin-top: 0.5rem;
  margin-bottom: 0;
  font-weight: 500;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  color: var(--text-muted);
  font-weight: 600;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
}

.form-label i {
  color: var(--c-secondary);
  font-size: 1.1rem;
}

.form-control, input[type="tel"], input[type="email"], input[type="password"], input[type="text"] {
  background: rgba(255, 255, 255, 0.03) !important;
  border: 1px solid var(--c-border) !important;
  color: var(--text-main) !important;
  padding: 0.85rem 1.25rem !important;
  border-radius: 12px !important;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
  font-size: 1rem !important;
}

input[type="tel"]:focus,
input[type="email"]:focus,
input[type="password"]:focus,
input[type="text"]:focus,
.form-control:focus {
  background: rgba(0, 0, 0, 0.2) !important;
  border-color: var(--c-primary) !important;
  color: var(--text-main) !important;
  box-shadow: 0 0 0 4px rgba(123, 97, 255, 0.1) !important;
  outline: none !important;
}

input[type="tel"]::placeholder,
input[type="email"]::placeholder,
input[type="password"]::placeholder,
input[type="text"]::placeholder,
.form-control::placeholder {
  color: rgba(255, 255, 255, 0.3) !important;
}

.form-text {
  color: var(--text-muted) !important;
  display: block;
  margin-top: 0.6rem;
  font-size: 0.85rem;
  opacity: 0.8;
}

.invalid-feedback {
  color: #ff6b6b !important;
  font-size: 0.85rem !important;
  margin-top: 0.5rem;
  font-weight: 500;
}

.btn-signup {
  background: linear-gradient(135deg, var(--c-secondary), var(--c-primary));
  border: none;
  color: white;
  font-weight: 700;
  border-radius: 12px;
  padding: 0.85rem;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 4px 15px rgba(123, 97, 255, 0.3);
  letter-spacing: 0.5px;
  margin-top: 1rem;
}

.btn-signup:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(123, 97, 255, 0.5);
  color: white;
}

.signup-footer {
  text-align: center;
  margin: 1.5rem 0 1rem;
  padding: 1.5rem 0 0;
  border-top: 1px solid var(--c-border);
}

.signup-footer p {
  color: var(--text-muted);
  margin: 0;
  font-size: 0.95rem;
}

.signup-footer a {
  color: var(--c-secondary);
  text-decoration: none;
  font-weight: 600;
  margin-left: 0.5rem;
  transition: color 0.3s;
}

.signup-footer a:hover {
  color: var(--c-primary);
  text-decoration: underline;
}

.alert {
  border: 1px solid rgba(231, 76, 60, 0.3) !important;
  background: rgba(231, 76, 60, 0.1) !important;
  color: #ff6b6b !important;
  border-radius: 12px !important;
  backdrop-filter: blur(5px);
}

.btn-outline-secondary {
    border-radius: 12px;
    padding: 0.85rem;
    border: 1px solid rgba(255,255,255,0.1);
    color: var(--text-muted);
    background: transparent;
    transition: all 0.3s;
}

.btn-outline-secondary:hover {
    background: rgba(255,255,255,0.05);
    color: var(--text-main);
    border-color: var(--c-border);
}

@media (max-width: 768px) {
  .signup-card {
    padding: 2rem 1.5rem;
  }

  .signup-title {
    font-size: 1.8rem;
  }
}
</style>
"""

# Process login.html
with open(login_path, 'r', encoding='utf-8') as f:
    login_lines = f.readlines()
    
with open(login_path, 'w', encoding='utf-8') as f:
    f.writelines(login_lines[:73])
    f.write(login_css)
    f.write('\n{% endblock content %}\n')

# Process registerUser.html
with open(register_path, 'r', encoding='utf-8') as f:
    reg_lines = f.readlines()
    
with open(register_path, 'w', encoding='utf-8') as f:
    f.writelines(reg_lines[:127])
    f.write(register_css)
    f.write('\n{% endblock content %}\n')

print("Success")
