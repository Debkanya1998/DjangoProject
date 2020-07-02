from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.

def login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = auth.authenticate(username=uname, password=pwd)
        if user is not None:
            auth.login(request, user)
            return redirect('/shop')
        else:
            return render(request, 'login.html', {'error': "Invalid Login Credentials"})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        #create a user
        if request.POST['password'] == request.POST['passwordagain']:
            try:
                user = User.objects.get(username=request.POST['username'], email=request.POST['email'])
                return render(request, 'register.html', {'error': "Username or Email has already been taken"})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
                auth.login(request, user)
                return redirect('/accounts/login')
        else:
            return render(request, 'register.html', {'error': "Passwords Don't Match"})
    else:
        return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')