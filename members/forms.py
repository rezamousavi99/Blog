from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    user_name = forms.CharField(max_length="20")
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class RegisterUserForm(UserCreationForm):
    # we were also able to not write these 3 fields since we configured them in Meta
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
