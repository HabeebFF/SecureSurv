from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

def login_page(request):
    return render(request, "auth/login.html")

def dashboard_page(request):
    return render(request, "dashboard/dashboard.html")