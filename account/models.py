from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from core.validators import DateValidator, PhoneValidator


class UserManager(BaseUserManager):
    '''
    User 생성 클래스
    '''

    def create_user(self, username, password=None):
        '''
        일반 User 생성 method

        Args:
            username:   User 이름
            password:   User 비밀번호

        Raises:
            ValueError: username이 입력되지 않은 경우

        Returns:
            생성된 User 객체
        '''
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        '''
        Amdin User 생성 method

        Args:
            username:   User 이름
            password:   User 비밀번호

        Returns:
            생성된 Admin User 객체

        '''
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    '''
    User 모델

    Fields:
        username(Char):     User 이름   
        is_admin(Bool):     Admin 권한 플래그
        is_artist(Bool):    작가 권한 플래그
        is_manager(Bool):   관리자 권한 플래그
    '''
    username = models.CharField(max_length=20, unique=True)
    is_admin = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        '''User 객체 출력 method'''
        return self.username

    def has_perm(self, perm, obj=None):
        '''주어진 object 권한 확인 method'''
        return True

    def has_module_perms(self, app_label):
        '''주어진 app 권한 확인 method'''
        return True

    @property
    def is_staff(self):
        '''Admin 권한 확인 method'''
        return self.is_admin


class Applyment(models.Model):
    '''
    작가등록신청 모델

    Fields:
        user(FK):           유저
        name(Char):         작가 이름
        gender(Char):       작가 성별
        birth_date(Date):   작가 생년월일
        email(Email):       작가 이메일
        phone(Char):        작가 연락처
        created_at(Date):   작가등록 신청일
        is_approved(Bool):  작가등록 승인 플래그
        is_rejected(Bool):  작가등록 반려 플래그
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    gender = models.CharField(max_length=5)
    birth_date = models.DateField(validators=[DateValidator])
    email = models.EmailField()
    phone = models.CharField(validators=[PhoneValidator], max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        '''Applyment 모델 출력 method'''
        return self.name
