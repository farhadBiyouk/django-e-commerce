from django import forms
from django.contrib.auth.models import User
from accounts.models import Profile

errors = {
    'required': 'این فیلد اجباری می باشد'
}


class UserRegisterForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50, error_messages=errors)
    last_name = forms.CharField(max_length=50)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_user_name(self):
        username = self.cleaned_data['user_name']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('this username is already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('this username is already exists')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('passwords not match')
        elif len(password1) < 5:
            raise forms.ValidationError('password was short')
        elif not any(ch.isupper() for ch in password2):
            raise forms.ValidationError('password must have is upper case')
        return password1


class UserLoginForm(forms.Form):
    user_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'username or email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'enter password'}))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'profile_image']
