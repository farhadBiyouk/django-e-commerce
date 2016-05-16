from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from accounts.forms import UserRegisterForm, UserLoginForm
from django.contrib import messages


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            User.objects.create_user(username=data['user_name'],
                                     password=data['password1'],
                                     first_name=data['first_name'],
                                     last_name=data['last_name'],
                                     email=data['email']

                                     )
            return redirect('home:home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['user_name'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'welcome to site')
                return redirect('home:home')
            else:
                messages.error(request, 'this operation have problem')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'با موفقیت از سایت خارج شدید')
    return redirect('home:home')
