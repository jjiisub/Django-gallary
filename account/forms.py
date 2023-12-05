from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Applyment, User


class UserCreateForm(UserCreationForm):
    '''
    User 로그인 Form

    Fields:
        username:   User 이름
        password1:  User 비밀번호
        password2:  User 비밀번호 확인
    '''
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class ApplymentCreateForm(forms.ModelForm):
    '''
    작가등록신청 Form

    Fields:
        name:       작가 이름
        gender:     작가 성별
        birth_date: 작가 생년월일
        email:      작가 이메일
        phone:      작가 연락처
    '''
    birth_date = forms.CharField(max_length=15)

    class Meta:
        model = Applyment
        fields = ['name', 'gender', 'birth_date', 'email', 'phone']
