from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from django.contrib.auth import logout

# Home Page
def home(request):
    return render(request, "home.html")

# Signup View
def signup(request):

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            from django.contrib.auth.models import User
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            return redirect("login")

    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


# Login View
def login_user(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:

            login(request, user)

            return redirect("welcome")

        else:
            return render(request, "login.html", {"error": "Invalid Username or Password"})

    return render(request, "login.html")


# Welcome Page
def welcome(request):
    return render(request, "welcome.html")

def logout_user(request):
    logout(request)
    return redirect('home')