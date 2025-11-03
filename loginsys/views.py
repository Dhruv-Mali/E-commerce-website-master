from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from django.http import HttpResponse
from store.models import Customer

def loginUser(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            return HttpResponse("Something went wrong")

    return render(request, 'loginsys/login.html')

def logoutUser(request):
    logout(request)
    return redirect('store')

def registerUser(request):
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Customer will be created automatically by the signal
            login(request, user)
            return redirect('store')

    context = {'form': form}
    return render(request, 'loginsys/registerUser.html', context)
