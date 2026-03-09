"""Secure authentication views with rate limiting and input validation"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.utils.html import escape
from django.core.cache import cache
from django.http import HttpResponseForbidden
import logging

logger = logging.getLogger(__name__)

from .forms import SignupForm
from apps.store.models import Customer

# Rate limiting configuration
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 900  # 15 minutes

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def check_rate_limit(request, action='login'):
    """Check if user has exceeded rate limit"""
    ip = get_client_ip(request)
    cache_key = f'auth_attempt_{action}_{ip}'
    attempts = cache.get(cache_key, 0)
    
    if attempts >= MAX_LOGIN_ATTEMPTS:
        return False
    
    cache.set(cache_key, attempts + 1, LOCKOUT_DURATION)
    return True

def sanitize_input(value, max_length=100):
    """Sanitize user input"""
    if not value:
        return ""
    return escape(str(value).strip()[:max_length])

@require_http_methods(["GET", "POST"])
@csrf_protect
def loginUser(request):
    """Secure user login with rate limiting"""
    if request.user.is_authenticated:
        return redirect('store')
    
    if request.method == 'POST':
        # Check rate limit
        if not check_rate_limit(request, 'login'):
            logger.warning(f"Login rate limit exceeded for IP: {get_client_ip(request)}")
            return HttpResponseForbidden("Too many login attempts. Please try again later.")
        
        username = sanitize_input(request.POST.get('username', ''), 150)
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Please provide both username and password')
            return render(request, 'loginsys/login.html')
        
        try:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                logger.info(f"User {username} logged in successfully")
                
                next_url = request.GET.get('next') or request.POST.get('next', '')
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect('store')
            else:
                logger.warning(f"Failed login attempt for username: {username}")
                messages.error(request, 'Invalid username or password')
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            messages.error(request, 'An error occurred during login')
    
    return render(request, 'loginsys/login.html')

@require_http_methods(["GET"])
def logoutUser(request):
    """Secure user logout"""
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('store')

@require_http_methods(["GET", "POST"])
@csrf_protect
def registerUser(request):
    """Secure user registration"""
    if request.user.is_authenticated:
        return redirect('store')
    
    # Check rate limit for registration
    if not check_rate_limit(request, 'register'):
        logger.warning(f"Registration rate limit exceeded for IP: {get_client_ip(request)}")
        return HttpResponseForbidden("Too many registration attempts. Please try again later.")
    
    form = SignupForm()
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                logger.info(f"New user registered: {user.username}")
                messages.success(request, 'Account created successfully!')
                return redirect('store')
            except Exception as e:
                logger.error(f"Registration error: {str(e)}")
                messages.error(request, 'Error creating account')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    
    context = {'form': form}
    return render(request, 'loginsys/registerUser.html', context)

@login_required(login_url='/l/')
@require_http_methods(["GET", "POST"])
@csrf_protect
def profile(request):
    """User profile management"""
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(
            user=request.user,
            name=request.user.username,
            email=request.user.email
        )
    
    if request.method == 'POST':
        name = sanitize_input(request.POST.get('name', ''), 100)
        email = sanitize_input(request.POST.get('email', ''), 255)
        
        if not name or not email:
            messages.error(request, 'Name and email are required')
            return render(request, 'loginsys/profile.html', {'customer': customer})
        
        try:
            customer.name = name
            customer.email = email
            customer.save()
            logger.info(f"Profile updated for user: {request.user.username}")
            messages.success(request, 'Profile updated successfully')
        except Exception as e:
            logger.error(f"Profile update error: {str(e)}")
            messages.error(request, 'Error updating profile')
        
        return redirect('profile')
    
    context = {'customer': customer}
    return render(request, 'loginsys/profile.html', context)
