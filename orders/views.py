from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/index.html", {"message": None})
    context = {
        "user": request.user
    }
    return render(request, "orders/user.html", context)


def login_view(request):
    return render(request, "orders/login.html")


def loggedin_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials. Please try again."})

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "You are now logged out."})

def signup_view(request):
    return render(request, "orders/signup.html")

def signupsuccess_view(request):


    username = request.POST["username"]
    password = request.POST["password"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]

    if User.objects.filter(username=username).exists():
        return render(request, "orders/signup.html", {"message": "ID already taken. Please try a different ID."})
    else:
        user = User.objects.create_user(username, password=password, email=email)
        user.last_name = last_name
        user.first_name = first_name
        user.save()
        return render(request, "orders/signupsuccess.html")
