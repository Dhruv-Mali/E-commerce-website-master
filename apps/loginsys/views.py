from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm
from apps.store.models import Customer

def loginUser(request):
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
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('store')
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
    
    if request.method == 'POST':
        customer.name = request.POST.get('name', '').strip()
        customer.email = request.POST.get('email', '').strip()
        if customer.name and customer.email:
            customer.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Name and email are required')
        return redirect('profile')
    
    context = {'customer': customer}
    return render(request, 'loginsys/profile.html', context)
