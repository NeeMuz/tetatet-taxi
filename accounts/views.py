from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is None:
            return render(request, "login.html", {"error": "Неверный email или пароль"})

        login(request, user)
        return redirect("/order/")

    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email уже используется"})

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        login(request, user)
        return redirect("/order/")

    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def order_page(request):
    return render(request, "order.html")
