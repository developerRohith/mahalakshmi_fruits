from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, ProfileForm
from .models import CustomerProfile


def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


def user_login(request):

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "accounts/login.html"
    )

def user_logout(request):
    logout(request)
    return redirect("home")

def profile(request):

    if not request.user.is_authenticated:
        return redirect("login")

    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
        }
    )