from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Applyment, User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class ApplymentCreateForm(forms.ModelForm):
    birth_date = forms.CharField(max_length=15)

    class Meta:
        model = Applyment
        fields = ['name', 'gender', 'birth_date', 'email', 'phone']
