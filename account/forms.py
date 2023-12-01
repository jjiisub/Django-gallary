from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

class UserCreateForm(UserCreationForm):
    username = forms.CharField(label='사용자ID')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
