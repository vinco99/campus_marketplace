from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "users/login.html")

def register(request):
    return render(request, "users/register.html")

def otp(request):
    return render(request, "users/otp.html")

def create_product(request):
    return render(request, "products/create_product.html")