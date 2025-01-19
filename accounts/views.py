from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from wheel.util import text_type

from accounts.forms import (
    UserRegisterForm,
    UserLoginForm,
    UserUpdateForm,
    ProfileUpdateForm
)
from django.contrib import messages
from accounts.models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMessage
from django.views import View
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from home.models import Product
from order.models import OrderItem


class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))


email_register = EmailToken()


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['user_name'],
                                            password=data['password1'],
                                            first_name=data['first_name'],
                                            last_name=data['last_name'],
                                            email=data['email']

                                            )
            user.is_active = False
            user.save()
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            url = reverse('accounts:active', kwargs={'uidb64': uidb64, 'token': email_register.make_token(user)})
            linke = 'http://' + domain + url
            mail = EmailMessage(
                'active user',
                linke,
                'test@gmail.com',
                [data['email']]
            )
            mail.send(fail_silently=True)
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
                messages.error(request, 'username or password wrong')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'با موفقیت از سایت خارج شدید')
    return redirect('home:home')


def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, 'accounts/profile.html', {'profile': profile})


def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'updated successfully')
            return redirect('accounts:user_profile')
        else:
            messages.error(request, 'the input is not valid')
            return redirect('accounts:update_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'accounts/update.html', {'user_form': user_form, 'profile_form': profile_form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'changed password successfully')
            return redirect('accounts:user_profile')
        else:
            messages.success(request, 'have problem for change password ')
            return redirect('accounts:change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change.html', {'form': form})


def favourites(request):
    product = request.user.fa_user.all()
    return render(request, 'accounts/favourite.html', {'product': product})


def history(request):
    data = OrderItem.objects.filter(user_id=request.user.id)
    return render(request, 'accounts/history.html', {'data': data})


class EmailRegister(View):
    def get(self, request, uidb64, token):
        id = force_str((urlsafe_base64_decode(uidb64)))
        user = User.objects.get(id=id)
        if user and email_register.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('accounts:user_login')


class ResetPassword(auth_view.PasswordResetView):
    template_name = 'accounts/reset.html'
    success_url = reverse_lazy('accounts:reset_done')
    email_template_name = 'accounts/link.html'


class ResetPasswordDone(auth_view.PasswordResetDoneView):
    template_name = 'accounts/done.html'


class ConfirmPassword(auth_view.PasswordResetConfirmView):
    template_name = 'accounts/confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class Complete(auth_view.PasswordResetCompleteView):
    template_name = 'accounts/complete.html'
