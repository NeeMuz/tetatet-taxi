from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            return render(request, "register.html", {
                "error": "Пользователь с таким email уже существует"
            })

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)
        return redirect('/order/')

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect('/order/')
        else:
            return render(request, "login.html", {"error": "Неверные данные"})

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect('/')


def order_view(request):
    return render(request, "order.html")
