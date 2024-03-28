
from . models import Customer

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method =='POST':
        uname = request.POST.get('username')
        phone_number = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request, "passwords didn't macth")
            return redirect('catalog:index')
        else:
            user = User.objects.create_user(uname, phone_number, pass1 )
            user.save()
            my_user = authenticate(request, username=uname, password=pass1)
            if my_user is not None:
                login(request,my_user)
            return redirect('catalog:index')
    return render(request,'register.html')

def login_fun(request):
    if request.method =='POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password')
        my_user = authenticate(request, username=uname, password=pass1)
        if my_user is not None:
            login(request,my_user)
            return redirect('catalog:index')
        else:
            messages.error(request, "username or password is incorrect")
            return redirect('login')
    return render(request,'login.html')

@login_required(login_url='login')
def logout_fun(request):
    logout(request)
    return redirect('login')
    
def profile(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
    else:

        customer = None

    context={"customer": customer}
    return render(request, 'profile.html', context)