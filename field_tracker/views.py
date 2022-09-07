from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.shortcuts import redirect, render
from django.contrib import messages
#import pyrebase


# Create your views here.

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        print("post")
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            print("valid")
            return redirect('base')
        else:
            messages.info(request,"Incorrect username or password")
            print("ok")
            return redirect('login')
    else:
        return render(request,'login.html')

def index(request):
    return render(request,'index.html')

def base(request):
    return render(request,"base.html")