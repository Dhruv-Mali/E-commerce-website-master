from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
import json
from .forms import SignupForm
from .otp_models import OTP, UserPhone
from .otp_service import OTPService
from apps.store.models import Customer


@require_http_methods(["GET", "POST"])
def otp_login(request):
    """OTP-based login - Step 1: Enter phone number"""
    
    if request.user.is_authenticated:
        return redirect('store')
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', '').strip()
        
        if not phone_number:
            messages.error(request, 'Please enter a phone number')
            return render(request, 'loginsys/otp_login.html')
        
        # Format phone number
        phone_number = OTPService.format_phone_number(phone_number)
        
        # Check if phone number is registered
        try:
            user_phone = UserPhone.objects.get(phone_number=phone_number)
        except UserPhone.DoesNotExist:
            messages.error(request, 'Phone number not registered. Please sign up first.')
            return render(request, 'loginsys/otp_login.html')
        
        # Delete old OTPs for this phone
        OTP.objects.filter(phone_number=phone_number).delete()
        
        # Create new OTP
        otp_instance = OTP.objects.create(
            phone_number=phone_number,
            otp_type=OTP.OTP_TYPE_LOGIN
        )
        
        # Send OTP
        success, message = OTPService.send_otp_sms(phone_number, otp_instance.otp_code)
        
        if success:
            # Store phone number in session for next step
            request.session['otp_phone'] = phone_number
            request.session['otp_id'] = otp_instance.id
            messages.success(request, f'OTP sent to {phone_number}')
            return redirect('verify_otp')
        else:
            messages.error(request, f'Failed to send OTP: {message}')
    
    return render(request, 'loginsys/otp_login.html')


@require_http_methods(["GET", "POST"])
def verify_otp(request):
    """Verify OTP - Step 2: Enter OTP and login"""
    
    phone_number = request.session.get('otp_phone')
    otp_id = request.session.get('otp_id')
    
    if not phone_number or not otp_id:
        messages.error(request, 'Invalid session. Please try again.')
        return redirect('otp_login')
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code', '').strip()
        
        if not otp_code:
            messages.error(request, 'Please enter OTP')
            return render(request, 'loginsys/verify_otp.html', {'phone': phone_number})
        
        try:
            otp_instance = OTP.objects.get(id=otp_id)
            is_valid, message = otp_instance.verify(otp_code)
            
            if is_valid:
                # Get user and login
                user_phone = UserPhone.objects.get(phone_number=phone_number)
                login(request, user_phone.user, backend='django.contrib.auth.backends.ModelBackend')
                
                # Clear session
                del request.session['otp_phone']
                del request.session['otp_id']
                
                messages.success(request, 'Logged in successfully with OTP!')
                return redirect('store')
            else:
                messages.error(request, message)
        
        except OTP.DoesNotExist:
            messages.error(request, 'Invalid OTP session. Please try again.')
            return redirect('otp_login')
    
    return render(request, 'loginsys/verify_otp.html', {'phone': phone_number})


@require_http_methods(["POST"])
def resend_otp(request):
    """Resend OTP if not received"""
    
    phone_number = request.session.get('otp_phone')
    
    if not phone_number:
        return JsonResponse({'success': False, 'message': 'Invalid session'})
    
    try:
        # Delete old OTP
        OTP.objects.filter(phone_number=phone_number).delete()
        
        # Create new OTP
        otp_instance = OTP.objects.create(
            phone_number=phone_number,
            otp_type=OTP.OTP_TYPE_LOGIN
        )
        
        # Send OTP
        success, message = OTPService.send_otp_sms(phone_number, otp_instance.otp_code)
        
        request.session['otp_id'] = otp_instance.id
        
        return JsonResponse({'success': success, 'message': message})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def loginUser(request):
    """Traditional username/password login"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Please provide both username and password')
            return render(request, 'loginsys/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'loginsys/login.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('store')


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('store')
    
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        phone_number = request.POST.get('phone_number', '').strip()
        
        if not phone_number:
            messages.error(request, 'Phone number is required')
            return render(request, 'loginsys/registerUser.html', {'form': form})
        
        # Format phone number
        phone_number = OTPService.format_phone_number(phone_number)
        
        # Check if phone already registered
        if UserPhone.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'This phone number is already registered')
            return render(request, 'loginsys/registerUser.html', {'form': form})
        
        if form.is_valid():
            try:
                user = form.save()
                # Create phone profile
                UserPhone.objects.create(
                    user=user,
                    phone_number=phone_number,
                    is_verified=False
                )
                
                # Create customer
                Customer.objects.get_or_create(
                    user=user,
                    defaults={'name': user.username, 'email': user.email}
                )
                
                # Redirect to verify phone (optional)
                messages.success(request, 'Account created successfully! You can now login with OTP or password.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

    context = {'form': form}
    return render(request, 'loginsys/registerUser.html', context)


@login_required
def profile(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(
            user=request.user,
            name=request.user.username,
            email=request.user.email
        )
    
    # Get phone profile
    try:
        phone_profile = request.user.phone_profile
    except:
        phone_profile = None
    
    if request.method == 'POST':
        customer.name = request.POST.get('name', '').strip()
        customer.email = request.POST.get('email', '').strip()
        if customer.name and customer.email:
            customer.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Name and email are required')
        return redirect('profile')
    
    context = {'customer': customer, 'phone_profile': phone_profile}
    return render(request, 'loginsys/profile.html', context)
