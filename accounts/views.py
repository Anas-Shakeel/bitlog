from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

from .forms import CreateUserForm

# These characters should not be in the usernames
# ILLEGAL_CHARS = """ \\/:;*?"'`|%/,"""


# Create your views here.
def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        # Authenticate the user
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        # Invalid Creds?
        if not user:
            return render(
                request,
                "accounts/login.html",
                {"form_error": "Invalid Credentials, try again!"},
            )

        # Login User
        login(request, user)

        # Redirect to Next_url (if any)
        next_url = request.GET.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("home")

    # Render the login page
    return render(request, "accounts/login.html")


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("accounts:login")


def signup_user(request):
    # Already Logged?
    if request.user.is_authenticated:
        return redirect("home")

    # Get the data
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # Create user and login
            user = form.save()
            login(request, user)

            messages.success(request, "Account created successfully!")

            return redirect("home")
    else:
        form = CreateUserForm()

    return render(request, "accounts/signup.html", {"form": form})
