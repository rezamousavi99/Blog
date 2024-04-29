from django.shortcuts import render
from .forms import LoginForm, RegisterUserForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.


def login_user(request):
    if request.method == "POST":
        user_name = request.POST['user_name']
        password = request.POST['password']

        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=user_name, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # messages.error(request, "This user has not found! have you ever signed up?")
                # return HttpResponseRedirect('/members/')
                error_massage = "Invalid username or password."
                return render(request, 'members/login.html', {
                    'error_massage': error_massage,
                    'login_form': form
                })
        else:
            return render(request, "members/login.html", {
            "login_form": form
        })

    else:
        return render(request, "members/login.html", {
            "login_form": LoginForm()
        })


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')

        return render(request, 'members/register.html', {
            'register_form': form
        })
    else:
        return render(request, 'members/register.html', {
            'register_form': RegisterUserForm()
        })