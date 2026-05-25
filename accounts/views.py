from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import User


def register_view(request):
    error = None

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            error = "Пользователь с таким email уже существует"
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            return redirect("login")

    return render(request, "register.html", {"error": error})


def login_view(request):
    error = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("order")
        else:
            error = "Неверный email или пароль"

    return render(request, "login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("login")


def order_page(request):
    return render(request, "order.html")
